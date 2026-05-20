from django.test import TestCase
from django.urls import reverse

from newhire.blog.models import Comment
from newhire.test import factories


class TestPostListView(TestCase):
    def setUp(self):
        self.user = factories.UserFactory()
        self.posts = [factories.PostFactory(author=self.user, published=True) for _ in range(25)]
        self.post_1 = factories.PostFactory(author=self.user, published=True)
        self.post_2 = factories.PostFactory(published=True)
        self.url = reverse("blogs:post-list")

    def test_get_post_list(self):
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert self.post_1.title in response.content.decode()
        assert self.post_2.title in response.content.decode()

    def test_post_list_hides_draft_posts(self):
        draft_post = factories.PostFactory(title="Draft Post")

        response = self.client.get(self.url)

        assert response.status_code == 200
        assert draft_post not in response.context["posts"]
        assert draft_post.title not in response.content.decode()

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
        matching_post = factories.PostFactory(title="Django Search Result", published=True)
        other_post = factories.PostFactory(title="Python Article", published=True)

        response = self.client.get(self.url + "?q=django")

        assert response.status_code == 200
        assert matching_post in response.context["posts"]
        assert other_post not in response.context["posts"]

    def test_post_list_search_by_body(self):
        matching_post = factories.PostFactory(body="Django Search Result", published=True)
        other_post = factories.PostFactory(body="Python Article", published=True)

        response = self.client.get(self.url + "?q=django")

        assert response.status_code == 200
        assert matching_post in response.context["posts"]
        assert other_post not in response.context["posts"]

    def test_post_list_search_by_author(self):
        matching_post = factories.PostFactory(author__name="Django Author", published=True)
        other_post = factories.PostFactory(author__name="Python Author", published=True)

        response = self.client.get(self.url + "?q=django")

        assert response.status_code == 200
        assert matching_post in response.context["posts"]
        assert other_post not in response.context["posts"]


class TestCategoryPostListView(TestCase):
    def setUp(self):
        self.category = factories.CategoryFactory(name="Django")
        self.other_category = factories.CategoryFactory(name="Python")
        self.post = factories.PostFactory(category=self.category, title="Django Post", published=True)
        self.other_post = factories.PostFactory(category=self.other_category, title="Python Post", published=True)
        self.url = reverse("blogs:post-category", args=[self.category.slug])

    def test_get_category_post_list(self):
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert self.post in response.context["posts"]
        assert self.other_post not in response.context["posts"]
        assert response.context["selected_category_slug"] == self.category.slug

    def test_get_category_post_list_hides_draft_posts(self):
        draft_post = factories.PostFactory(category=self.category)

        response = self.client.get(self.url)

        assert response.status_code == 200
        assert draft_post not in response.context["posts"]

    def test_get_category_post_list_with_invalid_category(self):
        url = reverse("blogs:post-category", args=["invalid-category"])
        response = self.client.get(url)

        assert response.status_code == 200
        assert len(response.context["posts"]) == 0

    def test_category_post_list_search_by_title(self):
        matching_post = factories.PostFactory(
            category=self.category,
            title="Django Search Result",
            published=True,
        )
        other_post = factories.PostFactory(
            category=self.category,
            title="Python Article",
            published=True,
        )

        response = self.client.get(self.url + "?q=django")

        assert response.status_code == 200
        assert matching_post in response.context["posts"]
        assert other_post not in response.context["posts"]


class TestTagPostListView(TestCase):
    def setUp(self):
        self.tag = factories.TagFactory(name="Django")
        self.other_tag = factories.TagFactory(name="Python")
        self.post = factories.PostFactory(title="Django Post", published=True)
        self.post.tags.add(self.tag)
        self.other_post = factories.PostFactory(title="Python Post", published=True)
        self.other_post.tags.add(self.other_tag)
        self.url = reverse("blogs:post-tag", args=[self.tag.slug])

    def test_get_tag_post_list(self):
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert self.post in response.context["posts"]
        assert self.other_post not in response.context["posts"]
        assert response.context["selected_tag_slug"] == self.tag.slug

    def test_get_tag_post_list_hides_draft_posts(self):
        draft_post = factories.PostFactory()
        draft_post.tags.add(self.tag)

        response = self.client.get(self.url)

        assert response.status_code == 200
        assert draft_post not in response.context["posts"]

    def test_get_tag_post_list_with_invalid_tag(self):
        url = reverse("blogs:post-tag", args=["invalid-tag"])
        response = self.client.get(url)

        assert response.status_code == 200
        assert len(response.context["posts"]) == 0

    def test_tag_post_list_search_by_title(self):
        matching_post = factories.PostFactory(title="Django Search Result", published=True)
        matching_post.tags.add(self.tag)
        other_post = factories.PostFactory(title="Python Article", published=True)
        other_post.tags.add(self.tag)

        response = self.client.get(self.url + "?q=django")

        assert response.status_code == 200
        assert matching_post in response.context["posts"]
        assert other_post not in response.context["posts"]


class TestPostDetailView(TestCase):
    def setUp(self):
        self.user = factories.UserFactory()
        self.post = factories.PostFactory(title="Test Post", body="Test Content", published=True)
        self.url = reverse("blogs:post-detail", args=[self.post.slug])

    def test_get_post_detail(self):
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert response.context["post"] == self.post

    def test_get_post_detail_with_invalid_slug(self):
        url = reverse("blogs:post-detail", args=["invalid-slug"])
        response = self.client.get(url)

        assert response.status_code == 404

    def test_get_post_detail_hides_draft_post(self):
        draft_post = factories.PostFactory()
        url = reverse("blogs:post-detail", args=[draft_post.slug])

        response = self.client.get(url)

        assert response.status_code == 404

    def test_authenticated_user_can_create_comment(self):
        commenter = factories.UserFactory()
        self.client.force_login(commenter)
        comment_data = {"body": "Test Comment"}

        response = self.client.post(self.url, comment_data)
        comment = Comment.objects.get(post=self.post, author=commenter)

        assert response.status_code == 302
        assert response.url == self.post.get_absolute_url()
        assert comment.body == "Test Comment"

    def test_authenticated_user_cannot_create_empty_comment(self):
        commenter = factories.UserFactory()
        self.client.force_login(commenter)

        response = self.client.post(self.url, {"body": ""})

        assert response.status_code == 200
        assert "form" in response.context
        assert "body" in response.context["form"].errors
        assert not Comment.objects.filter(post=self.post, author=commenter).exists()

    def test_unauthenticated_user_cannot_create_comment(self):
        comment_data = {"body": "Test Comment"}

        response = self.client.post(self.url, comment_data)

        assert response.status_code == 302
        assert "/accounts/login/" in response.url
        assert not Comment.objects.filter(post=self.post).exists()


class TestCommentDeleteView(TestCase):
    def setUp(self):
        self.user = factories.UserFactory()
        self.post = factories.PostFactory(author=self.user, published=True)
        self.comment = factories.CommentFactory(post=self.post)
        self.url = reverse("blogs:comment-delete", args=[self.comment.pk])

    def test_post_author_cannot_delete_comment(self):
        self.client.force_login(self.user)

        response = self.client.post(self.url)

        assert response.status_code == 404
        assert Comment.objects.filter(pk=self.comment.pk).exists()

    def test_comment_author_can_delete_comment(self):
        self.client.force_login(self.comment.author)

        response = self.client.post(self.url)

        assert response.status_code == 302
        assert response.url == self.post.get_absolute_url()
        assert not Comment.objects.filter(pk=self.comment.pk).exists()

    def test_unrelated_user_cannot_delete_comment(self):
        self.client.force_login(factories.UserFactory())

        response = self.client.post(self.url)

        assert response.status_code == 404
        assert Comment.objects.filter(pk=self.comment.pk).exists()

    def test_anonymous_user_cannot_delete_comment(self):
        response = self.client.post(self.url)

        assert response.status_code == 302
        assert "/accounts/login/" in response.url
        assert Comment.objects.filter(pk=self.comment.pk).exists()
