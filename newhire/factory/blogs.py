import factory

from newhire.blog.models import Category
from newhire.blog.models import Comment
from newhire.blog.models import Post
from newhire.blog.models import Tag
from newhire.users.tests.factories import UserFactory


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda number: f"Category {number}")


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Sequence(lambda number: f"Tag {number}")


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    author = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda number: f"Post {number}")
    body = "This is a sample post."
    category = factory.SubFactory(CategoryFactory)


class PublishedPostFactory(PostFactory):
    status = "published"


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    post = factory.SubFactory(PostFactory)
    author = factory.SubFactory(UserFactory)
    body = "This is a sample comment."
