from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps.common.models import AddressAbstractModel, VatPanAbstractModel


class Publisher(AddressAbstractModel, VatPanAbstractModel):

    publisher_name = models.CharField(
        max_length=255,
        verbose_name=_("Publisher name")
    )
    publisher_email = models.EmailField(
        max_length=255,
        verbose_name=_("Publisher email")
    )

    class Meta:
        verbose_name = _("Publisher")
        verbose_name_plural = _("Publishers")

    def __str__(self):
        return self.publisher_name
