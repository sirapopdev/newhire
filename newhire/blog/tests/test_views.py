from django.test import TestCase
from django.urls import reverse

from newhire.blog.models import Comment
from newhire.factory.blogs import (
    CategoryFactory,
    CommentFactory,
    PostFactory,
    TagFactory,
    UserFactory
)


class TestPostListView(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.posts = [PostFactory(author=self.user) for _ in range(25)]
        self.post_1 = PostFactory(author=self.user)
        self.post_2 = PostFactory()
        self.url = reverse("blogs:post-list")

    def test_get_post_list(self):
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert self.post_1.title in response.content.decode()
        assert self.post_2.title in response.content.decode()

    def test_post_list_pagination(self):
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert len(response.context["posts"]) == 10
        assert response.context["page_obj"].number == 1

    def test_first_page_returns_200(self):
        response = self.client.get(self.url)

        assert response.status_code == 200

    def test_second_page_returns_200(self):
        response = self.client.get(self.url + "?page=2")

        assert response.status_code == 200
        assert len(response.context["posts"]) == 10
        assert response.context["page_obj"].number == 2

    def test_post_list_search_by_title(self):
        matching_post = PostFactory(title="Django Search Result")
        other_post = PostFactory(title="Python Article")

        response = self.client.get(self.url + "?q=django")

        assert response.status_code == 200
        assert matching_post in response.context["posts"]
        assert other_post not in response.context["posts"]
    
    def test_post_list_search_by_body(self):
        matching_post = PostFactory(body="Django Search Result")
        other_post = PostFactory(body="Python Article")

        response = self.client.get(self.url + "?q=django")

        assert response.status_code == 200
        assert matching_post in response.context["posts"]
        assert other_post not in response.context["posts"]

    def test_post_list_search_by_author(self):
        matching_post = PostFactory(author__name="Django Author")
        other_post = PostFactory(author__name="Python Author")

        response = self.client.get(self.url + "?q=django")

        assert response.status_code == 200
        assert matching_post in response.context["posts"]
        assert other_post not in response.context["posts"]


class TestCategoryPostListView(TestCase):
    def setUp(self):
        self.category = CategoryFactory(name="Django")
        self.other_category = CategoryFactory(name="Python")
        self.post = PostFactory(category=self.category, title="Django Post")
        self.other_post = PostFactory(category=self.other_category, title="Python Post")
        self.url = reverse("blogs:post-category", args=[self.category.slug])

    def test_get_category_post_list(self):
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert self.post in response.context["posts"]
        assert self.other_post not in response.context["posts"]
        assert response.context["selected_category_slug"] == self.category.slug

    def test_get_category_post_list_with_invalid_category(self):
        url = reverse("blogs:post-category", args=["invalid-category"])
        response = self.client.get(url)

        assert response.status_code == 200
        assert len(response.context["posts"]) == 0

    def test_category_post_list_search_by_title(self):
        matching_post = PostFactory(category=self.category, title="Django Search Result")
        other_post = PostFactory(category=self.category, title="Python Article")

        response = self.client.get(self.url + "?q=django")

        assert response.status_code == 200
        assert matching_post in response.context["posts"]
        assert other_post not in response.context["posts"]


class TestTagPostListView(TestCase):
    def setUp(self):
        self.tag = TagFactory(name="Django")
        self.other_tag = TagFactory(name="Python")
        self.post = PostFactory(title="Django Post")
        self.post.tags.add(self.tag)
        self.other_post = PostFactory(title="Python Post")
        self.other_post.tags.add(self.other_tag)
        self.url = reverse("blogs:post-tag", args=[self.tag.slug])

    def test_get_tag_post_list(self):
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert self.post in response.context["posts"]
        assert self.other_post not in response.context["posts"]
        assert response.context["selected_tag_slug"] == self.tag.slug

    def test_get_tag_post_list_with_invalid_tag(self):
        url = reverse("blogs:post-tag", args=["invalid-tag"])
        response = self.client.get(url)

        assert response.status_code == 200
        assert len(response.context["posts"]) == 0

    def test_tag_post_list_search_by_title(self):
        matching_post = PostFactory(title="Django Search Result")
        matching_post.tags.add(self.tag)
        other_post = PostFactory(title="Python Article")
        other_post.tags.add(self.tag)

        response = self.client.get(self.url + "?q=django")

        assert response.status_code == 200
        assert matching_post in response.context["posts"]
        assert other_post not in response.context["posts"]


class TestPostDetailView(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.post = PostFactory(title="Test Post", body="Test Content")
        self.url = reverse("blogs:post-detail", args=[self.post.slug])

    def test_get_post_detail(self):
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert response.context["post"] == self.post

    def test_get_post_detail_with_invalid_slug(self):
        url = reverse("blogs:post-detail", args=["invalid-slug"])
        response = self.client.get(url)

        assert response.status_code == 404

    def test_authenticated_user_can_create_comment(self):
        commenter = UserFactory()
        self.client.force_login(commenter)
        comment_data = {"body": "Test Comment"}

        response = self.client.post(self.url, comment_data)
        comment = Comment.objects.get(post=self.post, author=commenter)

        assert response.status_code == 302
        assert response.url == self.post.get_absolute_url()
        assert comment.body == "Test Comment"

    def test_unauthenticated_user_cannot_create_comment(self):
        comment_data = {"body": "Test Comment"}

        response = self.client.post(self.url, comment_data)

        assert response.status_code == 302
        assert "/accounts/login/" in response.url
        assert not Comment.objects.filter(post=self.post).exists()


class TestCommentDeleteView(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.post = PostFactory(author=self.user)
        self.comment = CommentFactory(post=self.post)
        self.url = reverse("blogs:comment-delete", args=[self.comment.pk])

    def test_authenticated_user_can_delete_comment(self):
        self.client.force_login(self.user)

        response = self.client.post(self.url)

        assert response.status_code == 302
        assert response.url == self.post.get_absolute_url()
        assert not Comment.objects.filter(pk=self.comment.pk).exists()

    def test_anonymous_user_cannot_delete_comment(self):
        response = self.client.post(self.url)

        assert response.status_code == 302
        assert "/accounts/login/" in response.url
        assert Comment.objects.filter(pk=self.comment.pk).exists()
