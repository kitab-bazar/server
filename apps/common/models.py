from django.db import models
from django.utils.translation import ugettext_lazy as _


class NameUniqueAbstractModel(models.Model):
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=256,
        unique=True,
    )

    class Meta:
        abstract = True


class Province(NameUniqueAbstractModel):
    pass

    class Meta:
        verbose_name = _("Province")
        verbose_name_plural = _("Province")

    def __str__(self):
        return self.name


class District(NameUniqueAbstractModel):
    province = models.ForeignKey(
        'common.Province', verbose_name=_('Province'), related_name='%(app_label)s_%(class)s_province',
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = _("District")
        verbose_name_plural = _("Districts")

    def __str__(self):
        return self.name


class Municipality(models.Model):
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=256,
    )
    province = models.ForeignKey(
        'common.Province', verbose_name=_('Province'), related_name='%(app_label)s_%(class)s_province',
        on_delete=models.PROTECT
    )
    district = models.ForeignKey(
        'common.District', verbose_name=_('District'), related_name='%(app_label)s_%(class)s_district',
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = _("Municipality")
        verbose_name_plural = _("Municipalities")

    def __str__(self):
        return self.name


class AddressAbstractModel(models.Model):
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

    class Meta:
        abstract = True


class VatPanAbstractModel(models.Model):
    pan_number = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Pan number")
    )
    vat_number = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Vat number")
    )

    class Meta:
        abstract = True


class NameEmailAbstractModel(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name")
    )
    email = models.EmailField(
        max_length=255,
        verbose_name=_("Email")
    )

    class Meta:
        abstract = True
