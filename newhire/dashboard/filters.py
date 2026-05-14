import django_filters
from django.contrib.postgres.search import SearchQuery
from django.contrib.postgres.search import SearchVector

from newhire.blog.models import Category
from newhire.blog.models import Post


class PostFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(label="Search", method="filter_q")

    class Meta:
        model = Post
        fields = ()

    def filter_q(self, queryset, name, value):
        return queryset.annotate(
            search=SearchVector("title", "body", "author__name"),
        ).filter(search=SearchQuery(value))


class CategoryFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(label="Search", method="filter_q")

    class Meta:
        model = Category
        fields = ()

    def filter_q(self, queryset, name, value):
        return queryset.filter(name__icontains=value)
