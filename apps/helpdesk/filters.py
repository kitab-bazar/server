import django_filters
from apps.helpdesk.models import Faq
from django.db.models import Q


class FaqFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='search')

    class Meta:
        model = Faq
        fields = ()

    def search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(Q(question__icontains=value) | Q(answer__icontains=value))
