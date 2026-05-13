import django_filters
from django.db.models import Q

from newhire.blog.models import Category
from newhire.blog.models import Post


class PostFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(label="Search", method="filter_q")

    class Meta:
        model = Post
        fields = ()

    def filter_q(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value)
            | Q(body__icontains=value)
            | Q(author__name__icontains=value),
        )


class CategoryFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(label="Search", method="filter_q")

    class Meta:
        model = Category
        fields = ()

    def filter_q(self, queryset, name, value):
        return queryset.filter(name__icontains=value)
