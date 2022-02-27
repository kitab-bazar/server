from functools import reduce
import django_filters
from django.db import models
from django.conf import settings

from config.functions import StrPos
from apps.common.models import Province, Municipality, District
from utils.graphene.filters import IDListFilter


class SearchFilterMixin(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        search_fields = []

    def filter_search(self, queryset, _, value):
        if getattr(self.Meta, 'search_fields') is None:
            raise Exception('search_fields should be defined under Meta')
        if not value:
            return queryset
        print(
            reduce(
                lambda acc, item: acc | item,
                [
                    models.Q(**{f'{field}_{lang}__iexact': value})
                    for lang, _ in settings.LANGUAGES
                    for field in self.Meta.search_fields
                ],
            )
        )
        return queryset.filter(
            reduce(
                lambda acc, item: acc | item,
                [
                    models.Q(**{f'{field}_{lang}__icontains': value})
                    for lang, _ in settings.LANGUAGES
                    for field in self.Meta.search_fields
                ],
            )
        )


class ProvinceFilter(SearchFilterMixin, django_filters.FilterSet):
    class Meta:
        model = Province
        fields = ()
        search_fields = ('name',)


class MunicipalityFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    provinces = IDListFilter(method='filter_provinces')
    districts = IDListFilter(method='filter_districts')

    class Meta:
        model = Municipality
        fields = ()
        search_fields = ('name',)

    def filter_search(self, queryset, _, value):
        if value:
            return queryset.annotate(
                strpos_en=StrPos(
                    models.functions.Lower(
                        models.functions.Concat(
                            'district__province__name_en', models.Value(' '),
                            'district__name_en', models.Value(' '),
                            'name_en',
                            output_field=models.CharField()
                        )
                    ),
                    models.Value(value.lower(), models.CharField())
                ),
                strpos_ne=StrPos(
                    models.functions.Lower(
                        models.functions.Concat(
                            'district__province__name_ne', models.Value(' '),
                            'district__name_ne', models.Value(' '),
                            'name_ne',
                            output_field=models.CharField()
                        )
                    ),
                    models.Value(value.lower(), models.CharField())
                ),
            ).filter(
                models.Q(strpos_en__gte=1) | models.Q(strpos_ne__gte=1)
            ).order_by('strpos_en', 'strpos_ne')
        return queryset

    def filter_provinces(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(province__in=value)

    def filter_districts(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(district__in=value)


class DistrictFilter(SearchFilterMixin, django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    provinces = IDListFilter(method='filter_provinces')

    class Meta:
        model = District
        fields = ['name', ]
        search_fields = ('name',)

    def filter_search(self, queryset, _, value):
        if value:
            return queryset.annotate(
                strpos_en=StrPos(
                    models.functions.Lower(
                        models.functions.Concat(
                            'province__name_en', models.Value(' '), 'name_en',
                            output_field=models.CharField()
                        )
                    ),
                    models.Value(value.lower(), models.CharField())
                ),
                strpos_ne=StrPos(
                    models.functions.Lower(
                        models.functions.Concat(
                            'province__name_ne', models.Value(' '), 'name_ne',
                            output_field=models.CharField()
                        )
                    ),
                    models.Value(value.lower(), models.CharField())
                )
            ).filter(
                models.Q(strpos_en__gte=1) | models.Q(strpos_ne__gte=1)
            ).order_by('strpos_en', 'strpos_ne')
        return queryset

    def filter_provinces(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(province__in=value)
