from django.test import TestCase

from newhire.dashboard.tables import PostTable
from newhire.test import factories


class TestPostTable(TestCase):
    def setUp(self):
        self.category = factories.CategoryFactory(name="Django")
        self.user = factories.UserFactory(name="John Doe", email="john@example.com")
        self.post = factories.PostFactory(
            author=self.user,
            category=self.category,
            status="published",
        )
        self.table = PostTable([])

    def test_render_category_returns_category_name(self):
        assert self.table.render_category(self.post) == "Django"

    def test_render_category_returns_fallback_without_category(self):
        self.post.category = None

        assert self.table.render_category(self.post) == "No category"

    def test_render_status_returns_status_display(self):
        assert self.table.render_status(self.post) == "Published"

    def test_render_author_returns_author_name(self):
        assert self.table.render_author(self.post) == "John Doe"

    def test_render_author_returns_email_without_name(self):
        self.user.name = ""
        self.user.save()
        self.post.refresh_from_db()

        assert self.table.render_author(self.post) == "john@example.com"
