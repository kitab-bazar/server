import factory
from factory import fuzzy
from factory.django import DjangoModelFactory
from apps.common.models import Province, District, Municipality


class ProvinceFactory(DjangoModelFactory):
    name_en = fuzzy.FuzzyText(length=15)
    name_ne = fuzzy.FuzzyText(length=15)

    class Meta:
        model = Province


class DistrictFactory(DjangoModelFactory):
    name_en = fuzzy.FuzzyText(length=15)
    name_ne = fuzzy.FuzzyText(length=15)
    province = factory.SubFactory(ProvinceFactory)

    class Meta:
        model = District


class MunicipalityFactory(DjangoModelFactory):
    name_en = fuzzy.FuzzyText(length=15)
    name_ne = fuzzy.FuzzyText(length=15)
    province = factory.SubFactory(ProvinceFactory)
    province = factory.SubFactory(DistrictFactory)

    class Meta:
        model = Municipality
