import uuid

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


def activity_image_path(instance, filename):
    return f'activity-log/{type(instance)._meta.model_name}/{uuid.uuid4()}/{uuid.uuid4()}/{filename}'


class BaseActivityLogImage(models.Model):
    image = models.FileField(
        verbose_name=_('image'),
        upload_to=activity_image_path,
        null=True, blank=True
    )
    created_by = models.ForeignKey(
        'user.User', verbose_name=_('created by'),
        on_delete=models.PROTECT
    )

    def __str__(self):
        return self.image.url if self.image.url else str(self.id)


class BaseActivityLog(models.Model):
    comment = models.TextField(
        verbose_name=_('comment'),
        null=True, blank=True
    )
    system_comment = models.TextField(
        null=True, blank=True,
        verbose_name=_('system comment')
    )
    images = models.ManyToManyField(
        'common.BaseActivityLogImage', verbose_name=_('images'),
        blank=True
    )
    created_by = models.ForeignKey(
        'user.User', verbose_name=_('created by'),
        on_delete=models.PROTECT
    )

    class Meta:
        abstract = True
