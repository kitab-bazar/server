import factory
from factory import fuzzy
from factory.django import DjangoModelFactory

from apps.institution.models import Institution
from apps.common.factories import ProvinceFactory, DistrictFactory, MunicipalityFactory


class InstitutionFactory(DjangoModelFactory):
    name = fuzzy.FuzzyText(length=15)
    email = fuzzy.FuzzyText(length=15)
    pan_number = fuzzy.FuzzyText(length=15)
    vat_number = fuzzy.FuzzyText(length=15)
    province = factory.SubFactory(ProvinceFactory)
    district = factory.SubFactory(DistrictFactory)
    municipality = factory.SubFactory(MunicipalityFactory)
    ward_number = fuzzy.FuzzyInteger(1, 20)
    local_address = fuzzy.FuzzyText(length=15)

    class Meta:
        model = Institution
