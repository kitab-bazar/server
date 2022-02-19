from django.db import models
from django.utils.translation import gettext_lazy as _


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
