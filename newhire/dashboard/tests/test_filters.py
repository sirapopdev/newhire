from django.db import connection
from django.test import TestCase
from unittest import skipUnless

from newhire.dashboard.filters import CategoryFilter
from newhire.dashboard.filters import PostFilter
from newhire.factory.blogs import CategoryFactory
from newhire.factory.blogs import PostFactory
from newhire.factory.blogs import UserFactory


class TestCategoryFilter(TestCase):
    def setUp(self):
        self.matching_category = CategoryFactory(name="Django")
        self.other_category = CategoryFactory(name="Python")

    def test_filter_q_searches_category_name(self):
        category_filter = CategoryFilter(
            data={"q": "django"},
            queryset=CategoryFactory._meta.model.objects.all(),
        )

        assert self.matching_category in category_filter.qs
        assert self.other_category not in category_filter.qs


@skipUnless(connection.vendor == "postgresql", "PostFilter uses PostgreSQL full-text search")
class TestPostFilter(TestCase):
    def setUp(self):
        self.matching_author = UserFactory(name="Django Author")
        self.matching_title_post = PostFactory(title="Django Tips")
        self.matching_body_post = PostFactory(body="Django Content")
        self.matching_author_post = PostFactory(author=self.matching_author)
        self.other_post = PostFactory(title="Python Tips", body="Python Content")

    def test_filter_q_searches_title_body_and_author_name(self):
        post_filter = PostFilter(
            data={"q": "django"},
            queryset=PostFactory._meta.model.objects.all(),
        )

        assert self.matching_title_post in post_filter.qs
        assert self.matching_body_post in post_filter.qs
        assert self.matching_author_post in post_filter.qs
        assert self.other_post not in post_filter.qs
