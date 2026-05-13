import pytest
from django.urls import reverse

from newhire.blog.models import Category
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


def post_form_data(post, title="Updated Post"):
    return {
        "title": title,
        "body": "Updated content",
        "status": "published",
        "category": post.category.pk,
        "tags": [],
    }


def create_form_data(category, title="Created Post"):
    return {
        "title": title,
        "body": "Created content",
        "status": "published",
        "category": category.pk,
        "tags": [],
    }


def test_anonymous_user_cannot_access_post_create(client):
    url = reverse("dashboard_blogs:post-create")

    response = client.get(url)

    assert response.status_code == 302
    assert "/accounts/login/" in response.url


def test_anonymous_user_cannot_create_post(client):
    category = Category.objects.create(name="Anonymous Category")
    url = reverse("dashboard_blogs:post-create")

    response = client.post(url, create_form_data(category))

    assert response.status_code == 302
    assert "/accounts/login/" in response.url
    assert not Post.objects.filter(title="Created Post").exists()


def test_anonymous_user_cannot_access_post_edit(client, user):
    post = create_post(user)
    url = reverse("dashboard_blogs:post-edit", kwargs={"pk": post.pk})

    response = client.get(url)

    assert response.status_code == 302
    assert "/accounts/login/" in response.url


def test_anonymous_user_cannot_update_post(client, user):
    post = create_post(user)
    url = reverse("dashboard_blogs:post-edit", kwargs={"pk": post.pk})

    response = client.post(url, post_form_data(post, title="Anonymous Update"))

    post.refresh_from_db()

    assert response.status_code == 302
    assert "/accounts/login/" in response.url
    assert post.title == "Test Post"


def test_anonymous_user_cannot_access_post_delete(client, user):
    post = create_post(user)
    url = reverse("dashboard_blogs:post-delete", kwargs={"pk": post.pk})

    response = client.get(url)

    assert response.status_code == 302
    assert "/accounts/login/" in response.url


def test_anonymous_user_cannot_delete_post(client, user):
    post = create_post(user)
    url = reverse("dashboard_blogs:post-delete", kwargs={"pk": post.pk})

    response = client.post(url)

    assert response.status_code == 302
    assert "/accounts/login/" in response.url
    assert Post.objects.filter(pk=post.pk).exists()


def test_author_can_edit_own_post(client, user):
    post = create_post(user)
    url = reverse("dashboard_blogs:post-edit", kwargs={"pk": post.pk})

    client.force_login(user)
    response = client.get(url)

    assert response.status_code == 200
    assert "Test Post" in response.content.decode()


def test_author_can_update_own_post(client, user):
    post = create_post(user)
    url = reverse("dashboard_blogs:post-edit", kwargs={"pk": post.pk})

    client.force_login(user)
    response = client.post(url, post_form_data(post, title="Author Updated Post"))

    post.refresh_from_db()

    assert response.status_code == 302
    assert post.title == "Author Updated Post"


def test_author_cannot_access_other_users_post_edit(client, user):
    owner = UserFactory.create()
    post = create_post(owner)
    url = reverse("dashboard_blogs:post-edit", kwargs={"pk": post.pk})

    client.force_login(user)
    response = client.get(url)

    assert response.status_code in [403, 404]


def test_author_cannot_update_other_users_post(client, user):
    owner = UserFactory.create()
    post = create_post(owner)
    url = reverse("dashboard_blogs:post-edit", kwargs={"pk": post.pk})

    client.force_login(user)
    response = client.post(url, post_form_data(post, title="Wrong User Update"))

    post.refresh_from_db()

    assert response.status_code in [403, 404]
    assert post.title == "Test Post"


def test_author_can_delete_own_post(client, user):
    post = create_post(user)
    url = reverse("dashboard_blogs:post-delete", kwargs={"pk": post.pk})

    client.force_login(user)
    response = client.post(url)

    assert response.status_code == 302
    assert not Post.objects.filter(pk=post.pk).exists()


def test_author_cannot_delete_other_users_post(client, user):
    owner = UserFactory.create()
    post = create_post(owner)
    url = reverse("dashboard_blogs:post-delete", kwargs={"pk": post.pk})

    client.force_login(user)
    response = client.post(url)

    assert response.status_code in [403, 404]
    assert Post.objects.filter(pk=post.pk).exists()


def test_staff_can_access_any_post_edit(client):
    owner = UserFactory.create()
    staff_user = UserFactory.create(is_staff=True)
    post = create_post(owner)
    url = reverse("dashboard_blogs:post-edit", kwargs={"pk": post.pk})

    client.force_login(staff_user)
    response = client.get(url)

    assert response.status_code == 200


def test_staff_can_update_any_post(client):
    owner = UserFactory.create()
    staff_user = UserFactory.create(is_staff=True)
    post = create_post(owner)
    url = reverse("dashboard_blogs:post-edit", kwargs={"pk": post.pk})

    client.force_login(staff_user)
    response = client.post(url, post_form_data(post, title="Staff Updated Post"))

    post.refresh_from_db()

    assert response.status_code == 302
    assert post.title == "Staff Updated Post"


def test_staff_can_delete_any_post(client):
    owner = UserFactory.create()
    staff_user = UserFactory.create(is_staff=True)
    post = create_post(owner)
    url = reverse("dashboard_blogs:post-delete", kwargs={"pk": post.pk})

    client.force_login(staff_user)
    response = client.post(url)

    assert response.status_code == 302
    assert not Post.objects.filter(pk=post.pk).exists()
