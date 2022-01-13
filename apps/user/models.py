from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        """ Ensure that email is case insensitive when logging in """
        return self.get(email__iexact=email)


class User(AbstractUser):
    """ Custom User Model """

    class UserType(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        PUBLISHER = 'publisher', 'Publisher'
        INSTITUTIONAL_USER = 'institutional_user', 'Institutional User'
        SCHOOL_ADMIN = 'school_admin', 'School Admin'
        INDIVIDUAL_USER = 'individual_user', 'Individual User'

    # Delete unused fields
    username = None

    # Use email as username
    USERNAME_FIELD = "email"

    # removes email from REQUIRED_FIELDS
    REQUIRED_FIELDS = []

    email = models.EmailField(ugettext("Email address"), unique=True)
    first_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=ugettext("First name")
    )
    last_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=ugettext("Last name")
    )
    full_name = models.CharField(
        max_length=520,
        null=True,
        blank=True,
        verbose_name=ugettext("Full Name")
    )
    phone_number = PhoneNumberField(null=True, blank=True, unique=True)
    user_type = models.CharField(
        choices=UserType.choices, max_length=40,
        default=UserType.INDIVIDUAL_USER,
        verbose_name=ugettext("User Type")
    )
    institution = models.ForeignKey(
        'institution.Institution', verbose_name=ugettext('Institution'), related_name='%(app_label)s_%(class)s_institution',
        on_delete=models.CASCADE, null=True, blank=True
    )
    publisher = models.ForeignKey(
        'publisher.Publisher', verbose_name=ugettext('Publisher'), related_name='%(app_label)s_%(class)s_publisher',
        on_delete=models.CASCADE, null=True, blank=True
    )
    school = models.ForeignKey(
        'school.School', verbose_name=ugettext('School'), related_name='%(app_label)s_%(class)s_school',
        on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        verbose_name = ugettext("User")
        verbose_name_plural = ugettext("Users")

    # Use the model manager with no username
    objects = UserManager()

    def __str__(self):

        # Get name
        return (
            f"{self.first_name} {self.last_name}"
            if self.first_name and self.last_name
            else self.email
        )

    def save(self, *args, **kwargs):
        first_name = self.first_name if self.first_name else ""
        last_name = self.first_name if self.first_name else ""
        self.full_name = f'{first_name} {last_name}'
        super().save(*args, **kwargs)
