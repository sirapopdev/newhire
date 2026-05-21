from unittest.mock import ANY

from django.test import TestCase

from newhire.api.serializers import (CategorySerializer, CommentSerializer,
                                     PostSerializer)
from newhire.test.factories import CategoryFactory, CommentFactory, PostFactory


class TestCategorySerializer(TestCase):
    def setUp(self):
        self.category = CategoryFactory(name="Django")

    def test_serializes_category_fields(self):
        data = CategorySerializer(self.category).data

        assert data == {
            "id": self.category.id,
            "name": "Django",
            "slug": self.category.slug,
        }


class TestPostSerializer(TestCase):
    def setUp(self):
        self.post = PostFactory(title="API Post")

    def test_serializes_post_fields(self):
        data = PostSerializer(self.post).data

        assert data == {
            "id": self.post.id,
            "title": "API Post",
            "slug": self.post.slug,
            "body": self.post.body,
            "featured_image": None,
            "status": self.post.status,
            "created_at": ANY,
            "updated_at": ANY,
            "category": self.post.category.id,
            "tags": [],
            "author": self.post.author.id,
        }

    def test_author_is_read_only(self):
        serializer = PostSerializer(data={
            "title": "New Post",
            "body": "Body",
            "category": self.post.category.id,
            "author": 999,
        })

        assert serializer.is_valid()
        assert "author" not in serializer.validated_data

    def test_title_uses_model_max_length(self):
        serializer = PostSerializer(data={
            "title": "x" * 256,
            "body": "Body",
            "category": self.post.category.id,
        })

        assert not serializer.is_valid()
        assert "title" in serializer.errors

    def test_body_accepts_long_text(self):
        serializer = PostSerializer(data={
            "title": "New Post",
            "body": "x" * 101,
            "category": self.post.category.id,
        })

        assert serializer.is_valid()
        assert serializer.validated_data["body"] == "x" * 101


class TestCommentSerializer(TestCase):
    def setUp(self):
        self.comment = CommentFactory(body="Nice post")

    def test_serializes_comment_fields(self):
        data = CommentSerializer(self.comment).data

        assert data == {
            "id": self.comment.id,
            "post": self.comment.post.id,
            "author": self.comment.author.id,
            "body": "Nice post",
            "created_at": ANY,
        }

    def test_author_is_read_only(self):
        serializer = CommentSerializer(data={
            "post": self.comment.post.id,
            "body": "New comment",
            "author": 999,
        })

        assert serializer.is_valid()
        assert "author" not in serializer.validated_data
