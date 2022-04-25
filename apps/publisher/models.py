from django.db import models
from django.utils.translation import gettext_lazy as _


class Publisher(models.Model):

    class InternalCodeType(models.TextChoices):
        ENGLISH = 'parichaya', _('Parichaya')
        NEPALI = 'bhundipuran', _('Bhundipuran')
        MAITHALI = 'kathalaya', _('Kathalaya')
        THARU = 'ekata', _('Ekata')

    name = models.CharField(
        max_length=255,
        verbose_name=_("Name")
    )
    province = models.ForeignKey(
        'common.Province', verbose_name=_('Province'), related_name='%(app_label)s_%(class)s_province',
        on_delete=models.PROTECT
    )
    district = models.ForeignKey(
        'common.District', verbose_name=_('District'), related_name='%(app_label)s_%(class)s_district',
        on_delete=models.PROTECT
    )
    municipality = models.ForeignKey(
        'common.Municipality', verbose_name=_('Municipality'), related_name='%(app_label)s_%(class)s_municipality',
        on_delete=models.PROTECT
    )
    ward_number = models.IntegerField(verbose_name=_('Ward Number'))
    local_address = models.CharField(verbose_name=_('Local address'), max_length=255, null=True, blank=True)
    pan_number = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
        verbose_name=_("Pan number")
    )
    vat_number = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
        verbose_name=_("Vat number")
    )
    # This is used for incentive generation only
    internal_code = models.CharField(
        choices=InternalCodeType.choices, max_length=40, verbose_name=_('Internal code'),
        default=None, null=True
    )

    class Meta:
        verbose_name = _("Publisher")
        verbose_name_plural = _("Publishers")

    def __str__(self):
        return self.name
