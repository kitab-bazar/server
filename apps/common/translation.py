from modeltranslation.translator import register, TranslationOptions
from apps.common.models import Province, District, Municipality


@register(Province)
class NewsTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(District)
class DistrictTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Municipality)
class MunicipalityTranslationOptions(TranslationOptions):
    fields = ('name',)
