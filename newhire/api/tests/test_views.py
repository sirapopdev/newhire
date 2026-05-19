from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from newhire.blog.models import Category, Post, Comment
from newhire.factory.blogs import CategoryFactory, CommentFactory, PostFactory, UserFactory

class TestPostApiViewSet(TestCase):
    def setUp(self):
        self.post = PostFactory(title="API Post")
        self.url = reverse("api:post-list")
        self.detail_url = reverse("api:post-detail", args=[self.post.id])

    def test_get_posts(self):
        response = self.client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]["id"] == self.post.id

    def test_get_post_detail(self):
        response = self.client.get(self.detail_url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "API Post"

    def test_get_post_comments(self):
        comment = CommentFactory(post=self.post, body="Nice post")
        url = reverse("api:post-comments", args=[self.post.id])

        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]["id"] == comment.id

    def test_authenticated_user_can_create_post(self):
        user = UserFactory()
        category = CategoryFactory()
        self.client.force_login(user)

        response = self.client.post(self.url, {
            "title": "New Post",
            "body": "New Body",
            "status": "draft",
            "category": category.id,
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert Post.objects.get(title="New Post").author == user


class TestCategoryApiViewSet(TestCase):
    def setUp(self):
        self.category = CategoryFactory(name="Django")
        self.url = reverse("api:category-list")
        self.detail_url = reverse("api:category-detail", args=[self.category.id])

    def test_get_categories(self):
        response = self.client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]["id"] == self.category.id

    def test_get_category_detail(self):
        response = self.client.get(self.detail_url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Django"

    def test_get_category_posts(self):
        post = PostFactory(category=self.category)
        url = reverse("api:category-posts", args=[self.category.id])

        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]["id"] == post.id

    def test_authenticated_user_can_create_category(self):
        user = UserFactory()
        self.client.force_login(user)

        response = self.client.post(self.url, {"name": "Python"})

        assert response.status_code == status.HTTP_201_CREATED
        assert Category.objects.filter(name="Python").exists()


class TestCommentApiViewSet(TestCase):
    def setUp(self):
        self.comment = CommentFactory(body="First comment")
        self.url = reverse("api:comment-list")
        self.detail_url = reverse("api:comment-detail", args=[self.comment.id])

    def test_get_comments(self):
        response = self.client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]["id"] == self.comment.id

    def test_get_comment_detail(self):
        response = self.client.get(self.detail_url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["body"] == "First comment"

    def test_authenticated_user_can_create_comment(self):
        user = UserFactory()
        post = PostFactory()
        self.client.force_login(user)

        response = self.client.post(self.url, {
            "post": post.id,
            "body": "New comment",
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert Comment.objects.get(body="New comment").author == user
