from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps.common.models import AddressAbstractModel, VatPanAbstractModel


class School(AddressAbstractModel, VatPanAbstractModel):

    school_name = models.CharField(
        max_length=255,
        verbose_name=_("School name")
    )
    school_email = models.EmailField(
        max_length=255,
        verbose_name=_("School email")
    )

    class Meta:
        verbose_name = _("School")
        verbose_name_plural = _("Schools")

    def __str__(self):
        return self.school_name
