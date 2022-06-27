from django.utils.translation import gettext_lazy as _
from django.db import models


class School(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name")
    )
    province = models.ForeignKey(
        'common.Province', verbose_name=_('Province'), related_name='schools',
        on_delete=models.PROTECT
    )
    district = models.ForeignKey(
        'common.District', verbose_name=_('District'), related_name='schools',
        on_delete=models.PROTECT
    )
    municipality = models.ForeignKey(
        'common.Municipality', verbose_name=_('Municipality'), related_name='schools',
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
    school_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("School id")
    )

    class Meta:
        verbose_name = _("School")
        verbose_name_plural = _("Schools")

    def __str__(self):
        return self.name
