from django.test import TestCase

from newhire.api.serializers import CategorySerializer, CommentSerializer, PostSerializer
from newhire.factory.blogs import CategoryFactory, CommentFactory, PostFactory


class TestCategorySerializer(TestCase):
    def setUp(self):
        self.category = CategoryFactory(name="Django")

    def test_serializes_category_fields(self):
        data = CategorySerializer(self.category).data

        assert data["id"] == self.category.id
        assert data["name"] == "Django"
        assert data["slug"] == self.category.slug


class TestPostSerializer(TestCase):
    def setUp(self):
        self.post = PostFactory(title="API Post")

    def test_serializes_post_fields(self):
        data = PostSerializer(self.post).data

        assert data["id"] == self.post.id
        assert data["title"] == "API Post"
        assert data["slug"] == self.post.slug
        assert data["body"] == self.post.body
        assert data["status"] == self.post.status
        assert data["category"] == self.post.category.id
        assert data["author"] == self.post.author.id

    def test_author_is_read_only(self):
        serializer = PostSerializer(data={
            "title": "New Post",
            "body": "Body",
            "category": self.post.category.id,
            "author": 999,
        })

        assert serializer.is_valid()
        assert "author" not in serializer.validated_data


class TestCommentSerializer(TestCase):
    def setUp(self):
        self.comment = CommentFactory(body="Nice post")

    def test_serializes_comment_fields(self):
        data = CommentSerializer(self.comment).data

        assert data["id"] == self.comment.id
        assert data["post"] == self.comment.post.id
        assert data["author"] == self.comment.author.id
        assert data["body"] == "Nice post"

    def test_author_is_read_only(self):
        serializer = CommentSerializer(data={
            "post": self.comment.post.id,
            "body": "New comment",
            "author": 999,
        })

        assert serializer.is_valid()
        assert "author" not in serializer.validated_data
