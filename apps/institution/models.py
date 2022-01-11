from django.utils.translation import ugettext_lazy as _
from apps.common.models import AddressAbstractModel, VatPanAbstractModel, NameEmailAbstractModel


class Institution(AddressAbstractModel, VatPanAbstractModel, NameEmailAbstractModel):

    class Meta:
        verbose_name = _("Institution")
        verbose_name_plural = _("Institutions")

    def __str__(self):
        return self.name
