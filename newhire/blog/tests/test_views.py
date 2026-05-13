import pytest
from django.urls import reverse

from newhire.blog.models import Post, Category, Tag

pytestmark = pytest.mark.django_db


def create_post(user, title="Test Post", status="published", category=None):
    if category is None:
        category = Category.objects.create(name=f"Test {title}")
    
    return Post.objects.create(
        title=title,
        body="Test Content",
        author=user,
        status=status,
        category=category,
    )


def test_post_list_view_pagination(client, user):
    for number in range(12):
        create_post(user, title=f"Test Post {number}")

    url = reverse("blogs:post-list")
    response = client.get(url)

    assert response.status_code == 200
    assert "page_obj" in response.context
    assert response.context["is_paginated"] is True


def test_post_detail_view_by_slug(client, user):
    post = create_post(user, title="My Detail Post")

    url = reverse("blogs:post-detail", args=[post.slug])
    response = client.get(url)

    assert response.status_code == 200
    assert response.context["post"] == post


def test_post_detail_view_returns_404_for_missing_slug(client):
    url = reverse("blogs:post-detail", args=["missing-post"])
    response = client.get(url)

    assert response.status_code == 404


def test_post_list_can_filter_by_category(client, user):
    django_category = Category.objects.create(name='Django Test')
    python_category = Category.objects.create(name='Python Test')

    django_post = create_post(user, title='Django Post', category=django_category)
    python_post = create_post(user, title='Python Post', category=python_category)

    url = reverse('blogs:post-category', args=[django_category.slug]) 
    response = client.get(url)

    assert response.status_code == 200
    assert django_post in response.context['posts']
    assert python_post not in response.context['posts']


def test_post_list_can_filter_by_tag(client, user):
    django_tag = Tag.objects.create(name='Django Test')
    python_tag = Tag.objects.create(name='Python Test')

    django_post = create_post(user, title='Django Post')
    django_post.tags.add(django_tag)

    python_post = create_post(user, title='Python Post')
    python_post.tags.add(python_tag)

    url = reverse('blogs:post-tag', args=[django_tag.slug])
    response = client.get(url)

    assert response.status_code == 200
    assert django_post in response.context['posts']
    assert python_post not in response.context['posts']


def test_post_list_search_results(client, user):
    django_post = create_post(user, title='Django Post')
    python_post = create_post(user, title='Python Post')

    url = reverse('blogs:post-list') + '?q=django'
    response = client.get(url)

    assert response.status_code == 200
    assert django_post in response.context['posts']
    assert python_post not in response.context['posts']