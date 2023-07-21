from django.db.models import QuerySet, Q, Case, IntegerField, Value, When
from django_filters import rest_framework as filters

from clients.models import Client


class ClientFilter(filters.FilterSet):
    sortBy = filters.CharFilter(method='sort_by')
    search = filters.CharFilter(method='custom_search')

    class Meta:
        model = Client
        fields = ()

    def sort_by(self, queryset: QuerySet, _, value: str):
        sorting_by = self.request.query_params.get('sortBy', 'createdAt')
        sorting_dir = self.request.query_params.get('sortDir', 'desc')
        sort = '-' if sorting_dir == 'desc' else ''
        sort += sorting_by
        return queryset.order_by(sort)

    def custom_search(self, queryset: QuerySet, _, value: str):
        q1 = Q(name__istartswith=value)
        q2 = Q(surname__istartswith=value)
        q3 = Q(surname__icontains=value)
        q4 = Q(name__icontains=value)
        q5 = Q(children__name__icontains=value)
        q6 = Q(children__surname__icontains=value)
        q7 = Q(livingAddress__city__icontains=value)
        q8 = Q(livingAddress__street__icontains=value)
        return queryset.filter(
            q1 | q2 | q3 | q4 | q5 | q6 | q7 | q8
        ).annotate(
            search_ordering=Case(
                When(q1, then=Value(1)),
                When(q2, then=Value(2)),
                When(q3, then=Value(3)),
                When(q4, then=Value(4)),
                When(q5, then=Value(5)),
                When(q6, then=Value(6)),
                When(q7, then=Value(7)),
                When(q8, then=Value(8)),
                default=Value(100),
                output_field=IntegerField(),
            )
        ).order_by('search_ordering')
