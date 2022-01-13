import factory
from factory import fuzzy
from factory.django import DjangoModelFactory

from apps.school.models import School
from apps.common.factories import ProvinceFactory, DistrictFactory, MunicipalityFactory


class SchoolFactory(DjangoModelFactory):
    name = fuzzy.FuzzyText(length=15)
    pan_number = fuzzy.FuzzyText(length=15)
    vat_number = fuzzy.FuzzyText(length=15)
    province = factory.SubFactory(ProvinceFactory)
    district = factory.SubFactory(DistrictFactory)
    municipality = factory.SubFactory(MunicipalityFactory)
    ward_number = fuzzy.FuzzyInteger(1, 20)
    local_address = fuzzy.FuzzyText(length=15)

    class Meta:
        model = School
