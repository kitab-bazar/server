from django.utils.translation import ugettext_lazy as _
from apps.common.models import AddressAbstractModel, VatPanAbstractModel, NameEmailAbstractModel


class Publisher(AddressAbstractModel, VatPanAbstractModel, NameEmailAbstractModel):

    class Meta:
        verbose_name = _("Publisher")
        verbose_name_plural = _("Publishers")

    def __str__(self):
        return self.name
