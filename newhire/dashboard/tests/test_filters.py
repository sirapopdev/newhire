from django.test import TestCase

from newhire.dashboard.filters import CategoryFilter
from newhire.dashboard.filters import PostFilter
from newhire.test import factories


class TestCategoryFilter(TestCase):
    def setUp(self):
        self.matching_category = factories.CategoryFactory(name="Django")
        self.other_category = factories.CategoryFactory(name="Python")

    def test_filter_q_searches_category_name(self):
        category_filter = CategoryFilter(
            data={"q": "django"},
            queryset=factories.CategoryFactory._meta.model.objects.all(),
        )

        assert self.matching_category in category_filter.qs
        assert self.other_category not in category_filter.qs


class TestPostFilter(TestCase):
    def setUp(self):
        self.matching_author = factories.UserFactory(name="Django Author")
        self.matching_title_post = factories.PostFactory(title="Django Tips")
        self.matching_body_post = factories.PostFactory(body="Django Content")
        self.matching_author_post = factories.PostFactory(author=self.matching_author)
        self.other_post = factories.PostFactory(title="Python Tips", body="Python Content")

    def test_filter_q_searches_title_body_and_author_name(self):
        post_filter = PostFilter(
            data={"q": "django"},
            queryset=factories.PostFactory._meta.model.objects.all(),
        )

        assert self.matching_title_post in post_filter.qs
        assert self.matching_body_post in post_filter.qs
        assert self.matching_author_post in post_filter.qs
        assert self.other_post not in post_filter.qs
