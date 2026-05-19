from rest_framework import serializers

from newhire.blog.models import Category
from newhire.blog.models import Comment
from newhire.blog.models import Post

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "body",
            "status",
            "category",
            "author",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "slug", "author", "created_at", "updated_at"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "author",
            "body",
            "created_at",
        ]
        read_only_fields = ["id", "author", "created_at"]
