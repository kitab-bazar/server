from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.cache import cache
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
        MODERATOR = 'moderator', _('Moderator')
        PUBLISHER = 'publisher', _('Publisher')
        INSTITUTIONAL_USER = 'institutional_user', _('Institutional User')
        SCHOOL_ADMIN = 'school_admin', _('School Admin')
        INDIVIDUAL_USER = 'individual_user', _('Individual User')

    # Delete unused fields
    username = None

    # Use email as username
    USERNAME_FIELD = "email"

    # removes email from REQUIRED_FIELDS
    REQUIRED_FIELDS = []

    email = models.EmailField(_("Email address"), unique=True)
    first_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("First name")
    )
    last_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Last name")
    )
    full_name = models.CharField(
        max_length=520,
        blank=True,
        verbose_name=_("Full Name")
    )
    phone_number = PhoneNumberField(null=True, blank=True, unique=True)
    user_type = models.CharField(
        choices=UserType.choices, max_length=40,
        default=UserType.INDIVIDUAL_USER,
        verbose_name=_("User Type")
    )
    image = models.FileField(
        upload_to='user/images/', max_length=255, blank=True
    )
    institution = models.ForeignKey(
        'institution.Institution', verbose_name=_('Institution'), related_name='institution_user',
        on_delete=models.CASCADE, null=True, blank=True
    )
    publisher = models.ForeignKey(
        'publisher.Publisher', verbose_name=_('Publisher'), related_name='publisher_user',
        on_delete=models.CASCADE, null=True, blank=True
    )
    school = models.ForeignKey(
        'school.School', verbose_name=_('School'), related_name='school_user',
        on_delete=models.CASCADE, null=True, blank=True
    )
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='verified_by_user',
        null=True, blank=True, verbose_name=_('Verified by')
    )

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    # Use the model manager with no username
    objects = UserManager()

    def __str__(self):

        # Get name
        return (
            f"{self.first_name} {self.last_name}"
            if self.first_name and self.last_name
            else self.email
        )

    @staticmethod
    def _reset_login_cache(email: str):
        cache.delete_many([
            User._last_login_attempt_cache_key(email),
            User._login_attempt_cache_key(email),
        ])

    # login attempts related stuff

    @staticmethod
    def _set_login_attempt(email: str, value: int):
        return cache.set(User._login_attempt_cache_key(email), value)

    @staticmethod
    def _get_login_attempt(email: str):
        return cache.get(User._login_attempt_cache_key(email), 0)

    @staticmethod
    def _set_last_login_attempt(email: str, value: float):
        return cache.set(User._last_login_attempt_cache_key(email), value)

    @staticmethod
    def _get_last_login_attempt(email: str):
        return cache.get(User._last_login_attempt_cache_key(email), 0)

    @staticmethod
    def _last_login_attempt_cache_key(email: str) -> str:
        return f'{email}_lga_time'

    @staticmethod
    def _login_attempt_cache_key(email: str) -> str:
        return f'{email}_lga'

    def save(self, *args, **kwargs):
        self.full_name = self.get_full_name()
        super().save(*args, **kwargs)
