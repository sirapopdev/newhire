import pytest
from django.urls import reverse

from newhire.blog.models import Category
from newhire.blog.models import Comment
from newhire.blog.models import Post
from newhire.users.tests.factories import UserFactory

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


def create_comment(post, user, body="Test Comment"):
    return Comment.objects.create(
        post=post,
        author=user,
        body=body,
    )


def test_authenticated_user_can_create_comment(client, user):
    post = create_post(UserFactory.create())
    url = reverse("blogs:post-detail", args=[post.slug])

    client.force_login(user)
    response = client.post(url, {"body": "Nice post!"})

    comment = Comment.objects.get()

    assert response.status_code == 302
    assert response.url == post.get_absolute_url()
    assert comment.post == post
    assert comment.author == user
    assert comment.body == "Nice post!"


def test_anonymous_user_cannot_create_comment(client, user):
    post = create_post(user)
    url = reverse("blogs:post-detail", args=[post.slug])

    response = client.post(url, {"body": "Anonymous comment"})

    assert response.status_code == 302
    assert "/accounts/login/" in response.url
    assert not Comment.objects.exists()


def test_comment_author_cannot_delete_comment(client, user):
    post = create_post(UserFactory.create())
    comment = create_comment(post, user)
    url = reverse("dashboard_blogs:comment-delete", kwargs={"pk": comment.pk})

    client.force_login(user)
    response = client.post(url)

    assert response.status_code == 403
    assert Comment.objects.filter(pk=comment.pk).exists()


def test_post_author_cannot_delete_comment(client, user):
    commenter = UserFactory.create()
    post = create_post(user)
    comment = create_comment(post, commenter)
    url = reverse("dashboard_blogs:comment-delete", kwargs={"pk": comment.pk})

    client.force_login(user)
    response = client.post(url)

    assert response.status_code == 403
    assert Comment.objects.filter(pk=comment.pk).exists()


def test_staff_can_delete_comment(client, user):
    staff_user = UserFactory.create(is_staff=True)
    post = create_post(user)
    comment = create_comment(post, UserFactory.create())
    url = reverse("dashboard_blogs:comment-delete", kwargs={"pk": comment.pk})

    client.force_login(staff_user)
    response = client.post(url)

    assert response.status_code == 302
    assert response.url == reverse("dashboard_blogs:comment-list")
    assert not Comment.objects.filter(pk=comment.pk).exists()


def test_normal_user_cannot_delete_comment(client, user):
    post = create_post(UserFactory.create())
    comment = create_comment(post, UserFactory.create())
    url = reverse("dashboard_blogs:comment-delete", kwargs={"pk": comment.pk})

    client.force_login(user)
    response = client.post(url)

    assert response.status_code == 403
    assert Comment.objects.filter(pk=comment.pk).exists()


def test_anonymous_user_cannot_delete_comment(client, user):
    post = create_post(user)
    comment = create_comment(post, user)
    url = reverse("dashboard_blogs:comment-delete", kwargs={"pk": comment.pk})

    response = client.post(url)

    assert response.status_code == 302
    assert "/accounts/login/" in response.url
    assert Comment.objects.filter(pk=comment.pk).exists()


def test_post_comment_count(client, user):
    post = create_post(user)
    other_post = create_post(user, title="Other Post")

    create_comment(post, UserFactory.create(), body="First comment")
    create_comment(post, UserFactory.create(), body="Second comment")
    create_comment(other_post, UserFactory.create(), body="Other post comment")

    response = client.get(post.get_absolute_url())

    assert response.status_code == 200
    assert post.comments.count() == 2
    assert other_post.comments.count() == 1
    assert response.context["post"].comments.count() == 2
