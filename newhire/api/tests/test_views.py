from rest_framework import status

from django.test import TestCase
from django.urls import reverse

from newhire.blog.models import Category, Comment, Post
from newhire.test.factories import (CategoryFactory, CommentFactory,
                                    PostFactory, UserFactory)


class TestPostApiViewSet(TestCase):
    def setUp(self):
        self.post = PostFactory(title="API Post")
        self.url = reverse("api:post-list")
        self.detail_url = reverse("api:post-detail", args=[self.post.id])

    def test_get_posts(self):
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]["id"] == self.post.id

    def test_get_post_detail(self):
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.get(self.detail_url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "API Post"

    def test_get_post_comments(self):
        user = UserFactory()
        self.client.force_login(user)
        comment = CommentFactory(post=self.post, body="Nice post")
        url = reverse("api:post-comments", args=[self.post.id])

        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]["id"] == comment.id

    def test_authenticated_user_can_create_post(self):
        user = UserFactory()
        category = CategoryFactory()
        self.client.force_login(user)
        
        post_count = Post.objects.count()
        response = self.client.post(self.url, {
            "title": "New Post",
            "body": "New Body",
            "status": "draft",
            "category": category.id,
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert Post.objects.count() == post_count + 1
        assert Post.objects.get(title="New Post").author == user

    def test_authenticated_user_cannot_create_post_with_long_title(self):
        user = UserFactory()
        category = CategoryFactory()
        self.client.force_login(user)

        response = self.client.post(self.url, {
            "title": "x" * 256,
            "body": "New Body",
            "status": "draft",
            "category": category.id,
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"title": ["Ensure this field has no more than 255 characters."]}

    def test_authenticated_user_can_create_post_with_long_body(self):
        user = UserFactory()
        category = CategoryFactory()
        self.client.force_login(user)
        body = "x" * 101

        post_count = Post.objects.count()
        response = self.client.post(self.url, {
            "title": "New Post",
            "body": body,
            "status": "draft",
            "category": category.id,
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert Post.objects.count() == post_count + 1
        assert response.data["body"] == body

    def test_authenticated_user_cannot_update_post_with_long_title(self):
        user = UserFactory()
        self.client.force_login(user)

        response = self.client.put(self.detail_url, {
            "title": "x" * 256,
            "body": "Updated Body",
            "status": "draft",
            "category": self.post.category.id,
        }, content_type="application/json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"title": ["Ensure this field has no more than 255 characters."]}

    def test_authenticated_user_can_update_post_with_long_body(self):
        user = UserFactory()
        self.client.force_login(user)
        body = "x" * 101

        response = self.client.put(self.detail_url, {
            "title": "Updated Post",
            "body": body,
            "status": "draft",
            "category": self.post.category.id,
        }, content_type="application/json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["body"] == body


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

        category_count = Category.objects.count()
        response = self.client.post(self.url, {"name": "Python"})

        assert response.status_code == status.HTTP_201_CREATED
        assert Category.objects.count() == category_count + 1
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

        comment_count = Comment.objects.count()
        response = self.client.post(self.url, {
            "post": post.id,
            "body": "New comment",
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert Comment.objects.count() == comment_count + 1
        assert Comment.objects.get(body="New comment").author == user
