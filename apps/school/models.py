from django.utils.translation import ugettext_lazy as _
from apps.common.models import AddressAbstractModel, VatPanAbstractModel, NameEmailAbstractModel


class School(AddressAbstractModel, VatPanAbstractModel, NameEmailAbstractModel):

    class Meta:
        verbose_name = _("School")
        verbose_name_plural = _("Schools")

    def __str__(self):
        return self.Name
