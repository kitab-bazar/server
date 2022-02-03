from rest_framework import serializers
from phonenumber_field.formfields import PhoneNumberField

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

from apps.user.models import User
from apps.common.tasks import generic_email_sender
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import ugettext
from apps.publisher.serializers import PublisherSerializer, PublisherUpdateSerializer
from apps.school.serializers import SchoolSerializer, SchoolUpdateSerializer
from apps.institution.serializers import InstitutionSerializer, InstitutionUpdateSerializer
from apps.institution.models import Institution
from apps.school.models import School
from apps.publisher.models import Publisher


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password',)
        extra_kwargs = {'password': {'write_only': True}}


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError('Invalid Credentials')
        return dict(user=user)


class UserPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, password):
        if not self.instance.check_password(password):
            raise serializers.ValidationError('The password is invalid.')
        return password

    def validate_new_password(self, password):
        validate_password(password)
        return password

    def save(self, **kwargs):
        self.instance.set_password(self.validated_data['new_password'])
        self.instance.save()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    institution = InstitutionSerializer(required=False)
    school = SchoolSerializer(required=False)
    publisher = PublisherSerializer(required=False)

    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name', 'password', 'phone_number', 'user_type',
            'institution', 'publisher', 'school'
        ]

    def validate_password(self, password):
        validate_password(password)
        return password

    def validate_email(self, email):
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError('The email is already taken.')
        return email

    def save(self, **kwargs):
        instance = User.objects.create_user(
            first_name=self.validated_data.get('first_name', ''),
            last_name=self.validated_data.get('last_name', ''),
            email=self.validated_data['email'],
            password=self.validated_data['password'],
            user_type=self.validated_data.get('user_type', None),
            phone_number=self.validated_data.get('phone_number', None),
            is_active=False
        )
        if instance.user_type == User.UserType.INSTITUTIONAL_USER.value:
            institution_data = self.validated_data['institution']
            municipality = institution_data['municipality']
            institution_data['district'] = municipality.district
            institution_data['province'] = municipality.province
            institution = Institution.objects.create(**institution_data)
            instance.institution = institution
            instance.save()

        elif instance.user_type == User.UserType.PUBLISHER.value:
            publisher_data = self.validated_data['publisher']
            municipality = publisher_data['municipality']
            publisher_data['district'] = municipality.district
            publisher_data['province'] = municipality.province
            publisher = Publisher.objects.create(**publisher_data)
            instance.publisher = publisher
            instance.save()

        elif instance.user_type == User.UserType.SCHOOL_ADMIN.value:
            school_data = self.validated_data['school']
            municipality = school_data['municipality']
            school_data['district'] = municipality.district
            school_data['province'] = municipality.province
            school = School.objects.create(**school_data)
            instance.school = school
            instance.save()

        subject = ugettext("Activate your account.")
        message = ugettext("Please click on the link to confirm your registration")
        uid = urlsafe_base64_encode(force_bytes(instance.pk))
        token = default_token_generator.make_token(instance)
        button_url = f'{settings.CLIENT_URL}/activate/{uid}/{token}/'

        # Prepare message for email
        html_context = {
            "heading": ugettext("Activate your account"),
            "message": message,
            "button_text": ugettext("Activate Account"),
            "full_name": str(instance),
        }
        if button_url:
            html_context["button_url"] = button_url
        # Send an email for account activation to user
        generic_email_sender.delay(
            subject, message, [instance.email], html_context=html_context
        )
        return instance


class ActivateSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        uid = attrs.get('uid', None)
        token = attrs.get('token', None)
        try:
            uid = force_text(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return attrs
        raise serializers.ValidationError(ugettext('Activation link is not valid.'))


class GenerateResetPasswordTokenSerializer(serializers.Serializer):
    """
    Serializer for password forgot endpoint.
    """
    email = serializers.EmailField(write_only=True, required=True)

    def validate(self, attrs):
        email = attrs.get("email", None)
        button_url = None
        # if user exists for this email
        try:
            user = User.objects.get(email=email)
            # Generate password reset token and uid
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            # Get base url by profile type
            button_url = f'{settings.CLIENT_URL}/reset-password/{uid}/{token}/'
            message = ugettext(
                "We received a request to reset your account password. "
                "If you wish to do so, please click below. Otherwise, you may "
                "safely disregard this email."
            )
        # if no user exists for this email
        except User.DoesNotExist:
            # explanatory email message
            raise serializers.ValidationError(ugettext('User with this email does not exist.'))
        subject = ugettext("Reset password")
        html_context = {
            "heading": ugettext("Reset Password"),
            "message": message,
            "button_text": ugettext("Reset Password"),
        }
        if button_url:
            html_context["button_url"] = button_url
        generic_email_sender.delay(
            subject, message, [email], html_context=html_context
        )
        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for password reset endpoints.
    """

    password_reset_token = serializers.CharField(write_only=True, required=True)
    uid = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    def validate_new_password(self, password):
        validate_password(password)
        return password

    def validate(self, attrs):
        uid = attrs.get("uid", None)
        token = attrs.get("password_reset_token", None)
        new_password = attrs.get("new_password", None)

        try:
            uid = force_text(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return attrs
        raise serializers.ValidationError(ugettext('The token is invalid.'))


class UpdateProfileSerializer(serializers.ModelSerializer):
    institution = InstitutionUpdateSerializer(required=False)
    school = SchoolUpdateSerializer(required=False)
    publisher = PublisherUpdateSerializer(required=False)
    phone_number = PhoneNumberField(required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'image', 'publisher', 'school', 'institution')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_phone_number(self, phone_number):
        if User.objects.filter(phone_number=phone_number).exclude(id=self.context['request'].user.id).exists():
            raise serializers.ValidationError('User with this Phone number already exists.')
        return phone_number

    def _save_profile_data(self, user, data):
        data_key = {
            User.UserType.INSTITUTIONAL_USER.value: 'institution',
            User.UserType.SCHOOL_ADMIN.value: 'school',
            User.UserType.PUBLISHER.value: 'publisher',
        }.get(user.user_type)

        serializer_class = {  # Used to create/update profile data.
            User.UserType.INSTITUTIONAL_USER.value: InstitutionSerializer,
            User.UserType.SCHOOL_ADMIN.value: SchoolSerializer,
            User.UserType.PUBLISHER.value: InstitutionSerializer,
        }.get(user.user_type)

        data = self.validated_data.pop(data_key, None)
        # NOTE: Serialier validated_data provides municipality object, but we have to pass id
        data['municipality'] = data['municipality'].id
        instance = getattr(user, data_key)
        serializer = serializer_class(data=data, instance=instance, partial=True)
        if not serializer.is_valid():
            raise serializers.ValidationError(serializer.errors)
        return serializer.save()

    def save(self, **kwargs):
        instance = self.context['request'].user
        # NOTE: Individual user don't have profile
        if instance.user_type != User.UserType.INDIVIDUAL_USER.value:
            self._save_profile_data(instance, self.validated_data)
        return super().update(instance, self.validated_data)
