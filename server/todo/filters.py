import django_filters
from django.db.models import Q, QuerySet
from django_filters import FilterSet

from todo.models import Task


class TaskFilter(FilterSet):
    title = django_filters.CharFilter(label="Title", method="filter_title_keywords")
    completed = django_filters.BooleanFilter(label="Is completed", field_name="completed")

    def filter_title_keywords(self, queryset: QuerySet, _: str, value: str | None) -> QuerySet:
        keywords = value.strip().split()
        if not keywords:
            return queryset
        query = Q()
        for keyword in keywords:
            query |= Q(title__icontains=keyword)
        return queryset.filter(query)

    class Meta:
        model = Task
        fields = ["title", "completed"]
