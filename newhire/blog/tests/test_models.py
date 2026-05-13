import pytest

from newhire.blog.models import Category, Comment, Post, Tag

pytestmark = pytest.mark.django_db

def test_post_slug_auto_generation(user):
    category = Category.objects.create(name='Test Category')

    post = Post.objects.create(
        title='Test Post',
        body='Test Content',
        author=user,
        category=category
    )

    assert post.slug == 'test-post'


def test_post_status_defaults_to_draft(user):
    category = Category.objects.create(name='Test Category')

    post = Post.objects.create(
        title='Test Post',
        body='Test Content',
        author=user,
        category=category
    )

    assert post.status == 'draft'

def test_category_str_representation():
    category = Category.objects.create(name='Test Category')
    assert str(category) == 'Test Category'

def test_tag_str_representation():
    tag = Tag.objects.create(name='Test Tag')
    assert str(tag) == 'Test Tag'

def test_comment_str_representation(user):
    category = Category.objects.create(name='Test Category')
    post = Post.objects.create(
        title='Test Post',
        body='Test Content',
        author=user,
        category=category
    )
    comment = Comment.objects.create(
        post=post,
        author=user,
        body='Test Comment'
    )
    assert str(comment) == f"Comment by {user} on {post}"