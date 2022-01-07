from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps.common.models import AddressAbstractModel, VatPanAbstractModel


class Institution(AddressAbstractModel, VatPanAbstractModel):

    institution_name = models.CharField(
        max_length=255,
        verbose_name=_("Institution name")
    )
    institution_email = models.EmailField(
        max_length=255,
        verbose_name=_("Institution email")
    )

    class Meta:
        verbose_name = _("Institution")
        verbose_name_plural = _("Institutions")

    def __str__(self):
        return self.institution_name
