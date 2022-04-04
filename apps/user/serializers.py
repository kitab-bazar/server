import time
from django.utils import timezone
from rest_framework import serializers
from django.core.cache import cache

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext

from apps.user.models import User
from apps.common.tasks import generic_email_sender
from apps.publisher.serializers import PublisherSerializer, PublisherUpdateSerializer
from apps.school.serializers import SchoolSerializer, SchoolUpdateSerializer
from apps.institution.serializers import InstitutionSerializer, InstitutionUpdateSerializer
from apps.institution.models import Institution
from apps.school.models import School
from apps.publisher.models import Publisher
from utils.validations import validate_hcaptcha, MissingCaptchaException


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password',)
        extra_kwargs = {'password': {'write_only': True}}


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    captcha = serializers.CharField(required=False, allow_null=True, write_only=True)
    site_key = serializers.CharField(required=False, allow_null=True, write_only=True)

    def _validate_captcha(self, attrs):
        captcha = attrs.get('captcha')
        site_key = attrs.get('site_key')
        email = attrs.get('email')
        attempts = User._get_login_attempt(email)

        def throttle_login_attempt():
            if attempts >= settings.MAX_CAPTCHA_LOGIN_ATTEMPTS:
                now = time.mktime(timezone.now().timetuple())
                last_tried = User._get_last_login_attempt(email)
                if not last_tried:
                    User._set_last_login_attempt(email, now)
                    raise serializers.ValidationError(
                        gettext('Please try again in %s seconds.') % settings.LOGIN_TIMEOUT
                    )
                elapsed = now - last_tried
                if elapsed < settings.LOGIN_TIMEOUT:
                    raise serializers.ValidationError(
                        gettext('Please try again in %s seconds.') % (settings.LOGIN_TIMEOUT - int(elapsed))
                    )
                else:
                    # reset
                    User._reset_login_cache(email)

        if attempts >= settings.MAX_LOGIN_ATTEMPTS and not captcha:
            raise MissingCaptchaException()
        if attempts >= settings.MAX_LOGIN_ATTEMPTS and captcha and not validate_hcaptcha(captcha, site_key):
            attempts = User._get_login_attempt(email)
            User._set_login_attempt(email, attempts + 1)

            throttle_login_attempt()
            raise serializers.ValidationError(dict(
                captcha=gettext('The captcha is invalid.')
            ))

    def validate(self, attrs):
        if cache.get('enable_captcha'):
            self._validate_captcha(attrs)
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                raise serializers.ValidationError(
                    gettext('Your accout is not active, please click the activation link we sent to your email')
                )
            if user.is_deactivated:
                raise serializers.ValidationError(
                    gettext('Your accout deactivated, please contact administrator')
                )
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError('Invalid Credentials')
        user = authenticate(email=email, password=password)
        if not user:
            attempts = User._get_login_attempt(email)
            User._set_login_attempt(email, attempts + 1)
            raise serializers.ValidationError('Invalid Credentials')
        User._reset_login_cache(email)
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
    captcha = serializers.CharField(required=False, write_only=True)
    site_key = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name', 'password', 'phone_number', 'user_type',
            'institution', 'publisher', 'school', 'captcha', 'site_key'
        ]

    def validate_site_key(self, captcha):
        if cache.get('enable_captcha'):
            raise serializers.ValidationError('This field is required')

    def validate_password(self, password):
        validate_password(password)
        return password

    def validate_email(self, email):
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError('The email is already taken.')
        return email

    def validate_user_type(self, user_type):
        if user_type == User.UserType.MODERATOR:
            raise serializers.ValidationError('Registration as moderator is not allowed.')
        return user_type

    def validate_captcha(self, captcha):
        if cache.get('enable_captcha'):
            if not validate_hcaptcha(captcha, self.initial_data.get('site_key', '')):
                raise serializers.ValidationError(dict(
                    captcha=gettext('The captcha is invalid.')
                ))

    def save(self, **kwargs):
        instance = User.objects.create_user(
            first_name=self.validated_data.get('first_name', ''),
            last_name=self.validated_data.get('last_name', ''),
            email=self.validated_data['email'],
            password=self.validated_data['password'],
            user_type=self.validated_data.get('user_type', None),
            phone_number=self.validated_data.get('phone_number', None),
            is_active=True
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

        subject = gettext("Activate your account.")
        message = gettext("Please click on the link to confirm your registration")
        uid = urlsafe_base64_encode(force_bytes(instance.pk))
        token = default_token_generator.make_token(instance)
        button_url = f'{settings.CLIENT_URL}/activate/{uid}/{token}/'

        # Prepare message for email
        html_context = {
            "heading": gettext("Activate your account"),
            "message": message,
            "button_text": gettext("Activate Account"),
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
        raise serializers.ValidationError(gettext('Activation link is not valid.'))


class GenerateResetPasswordTokenSerializer(serializers.Serializer):
    """
    Serializer for password forgot endpoint.
    """
    email = serializers.EmailField(write_only=True, required=True)
    captcha = serializers.CharField(required=False, write_only=True)
    site_key = serializers.CharField(required=False, write_only=True)

    def validate_captcha(self, captcha):
        if cache.get('enable_captcha'):
            if not validate_hcaptcha(captcha, self.initial_data.get('site_key', '')):
                raise serializers.ValidationError(dict(
                    captcha=gettext('The captcha is invalid.')
                ))

    def validate(self, attrs):
        if cache.get('enable_captcha'):
            raise serializers.ValidationError(dict(
                captcha=gettext('The captcha is invalid.')
            ))
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
            message = gettext(
                "We received a request to reset your account password. "
                "If you wish to do so, please click below. Otherwise, you may "
                "safely discard this email."
            )
        # if no user exists for this email
        except User.DoesNotExist:
            # explanatory email message
            raise serializers.ValidationError(gettext('User with this email does not exists'))
        subject = gettext("Reset password")
        html_context = {
            "heading": gettext("Reset Password"),
            "message": message,
            "button_text": gettext("Reset Password"),
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
        raise serializers.ValidationError(gettext('The token is invalid.'))


class UpdateProfileSerializer(serializers.ModelSerializer):
    institution = InstitutionUpdateSerializer(required=False)
    school = SchoolUpdateSerializer(required=False)
    publisher = PublisherUpdateSerializer(required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'image', 'publisher', 'school', 'institution')
        extra_kwargs = {'password': {'write_only': True}}

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


class UserVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ()

    def update(self, instance, _):
        instance.is_verified = True
        instance.verified_by = self.context['request'].user
        instance.save(update_fields=('is_verified', 'verified_by'))
        return instance


class UserDeactivateToggleSerializer(serializers.ModelSerializer):
    is_deactivated = serializers.BooleanField(required=True)

    class Meta:
        model = User
        fields = ('id', 'is_deactivated',)

    def validate_is_deactivated(self, is_deactivated):
        if self.instance.is_verified:
            raise serializers.ValidationError(gettext('Can not activate/deactivate verifield user'))
        return is_deactivated

    def update(self, instance, _):
        instance.is_deactivated_by = self.context['request'].user
        instance.is_deactivated = self.validated_data['is_deactivated']
        instance.save(update_fields=('is_deactivated', 'is_deactivated_by'))
        return instance
