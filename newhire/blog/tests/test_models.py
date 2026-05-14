from django.templatetags.static import static
from django.test import TestCase
from django.urls import reverse

from newhire.factory.blogs import (
    CategoryFactory,
    CommentFactory,
    PostFactory,
    TagFactory,
    UserFactory,
)


class TestCategoryModel(TestCase):
    def setUp(self):
        self.category = CategoryFactory(name="Django Python")

    def test_str_returns_name(self):
        assert str(self.category) == "Django Python"

    def test_slug_is_generated_from_name(self):
        assert self.category.slug == "django-python"
        assert self.category.slug == self.category.name.lower().replace(" ", "-")


class TestTagModel(TestCase):
    def setUp(self):
        self.tag = TagFactory(name="Python 3")

    def test_str_returns_name(self):
        assert str(self.tag) == "Python 3"

    def test_slug_is_generated_from_name(self):
        assert self.tag.slug == "python-3"
        assert self.tag.slug == self.tag.name.lower().replace(" ", "-")


class TestPostModel(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.category = CategoryFactory()
        self.post = PostFactory(
            author=self.user,
            category=self.category,
            title="My Blog Post",
        )

    def test_str_returns_title(self):
        assert str(self.post) == "My Blog Post"

    def test_slug_is_generated_from_title(self):
        assert self.post.slug == "my-blog-post"
        assert self.post.slug == self.post.title.lower().replace(" ", "-")

    def test_status_defaults_to_draft(self):
        assert self.post.status == "draft"

    def test_get_absolute_url_returns_detail_url(self):
        assert self.post.get_absolute_url() == reverse("blogs:post-detail", args=[self.post.slug])

    def test_featured_image_url_returns_static_fallback_without_image(self):
        self.post.featured_image = None

        assert self.post.featured_image_url == static("images/no-image.png")

    def test_post_can_have_tags(self):
        tag = TagFactory()

        self.post.tags.add(tag)

        assert tag in self.post.tags.all()
        assert self.post in tag.posts.all()

    def test_author_related_name_returns_blog_posts(self):
        assert self.post in self.user.blog_posts.all()

    def test_category_related_name_returns_posts(self):
        assert self.post in self.category.posts.all()


class TestCommentModel(TestCase):
    def setUp(self):
        self.user = UserFactory(name="John Doe")
        self.post = PostFactory(title="My Blog Post")
        self.comment = CommentFactory(post=self.post, author=self.user)

    def test_str_returns_author_and_post(self):
        assert str(self.comment) == f"Comment by {self.user} on {self.post}"

    def test_post_related_name_returns_comments(self):
        assert self.comment in self.post.comments.all()

    def test_author_related_name_returns_comments(self):
        assert self.comment in self.user.comments.all()
