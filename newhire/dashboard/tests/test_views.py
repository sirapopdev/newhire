from django.test import TestCase
from django.urls import reverse

from newhire.blog.models import Post, Category, Comment
from newhire.test import factories


class TestStaffRequiredMixin(TestCase):
    def setUp(self):
        self.user = factories.UserFactory(is_staff=False)
        self.staff_user = factories.UserFactory(is_staff=True)
        self.category = factories.CategoryFactory()
        self.post = factories.PostFactory(author=self.staff_user, category=self.category)
        self.comment = factories.CommentFactory(post=self.post)
        self.urls = [
            reverse("dashboard_blogs:post-list"),
            reverse("dashboard_blogs:post-create"),
            reverse("dashboard_blogs:post-edit", args=[self.post.pk]),
            reverse("dashboard_blogs:post-delete", args=[self.post.pk]),
            reverse("dashboard_blogs:category-list"),
            reverse("dashboard_blogs:category-create"),
            reverse("dashboard_blogs:category-edit", args=[self.category.pk]),
            reverse("dashboard_blogs:category-delete", args=[self.category.pk]),
            reverse("dashboard_blogs:comment-list"),
            reverse("dashboard_blogs:comment-delete", args=[self.comment.pk]),
        ]

    def test_anonymous_user_is_redirected_to_login(self):
        for url in self.urls:
            response = self.client.get(url)

            assert response.status_code == 302
            assert "/accounts/login/" in response.url

    def test_normal_user_gets_permission_denied(self):
        self.client.force_login(self.user)

        for url in self.urls:
            response = self.client.get(url)

            assert response.status_code == 403

    def test_staff_user_can_access_dashboard_views(self):
        self.client.force_login(self.staff_user)

        for url in self.urls:
            response = self.client.get(url)

            assert response.status_code == 200


class TestIndexView(TestCase):
    def setUp(self):
        self.staff_user = factories.UserFactory(is_staff=True)
        self.categories = [factories.CategoryFactory() for _ in range(5)]
        self.posts = [factories.PostFactory(category=self.categories[0]) for _ in range(15)]
        self.comments = [factories.CommentFactory(post=self.posts[0]) for _ in range(10)]
        self.url = reverse("dashboard:index")

    def test_get_index_view_context(self):
        self.client.force_login(self.staff_user)

        response = self.client.get(self.url)

        assert response.status_code == 200
        assert response.context["total_posts"] == 15
        assert response.context["total_categories"] == 5
        assert response.context["total_comments"] == 10


class TestDashboardPostListView(TestCase):
    def setUp(self):
        self.staff_user = factories.UserFactory(is_staff=True)
        self.category = factories.CategoryFactory()
        self.posts = [
            factories.PostFactory(author=self.staff_user, category=self.category)
            for _ in range(15)
        ]
        self.url = reverse("dashboard_blogs:post-list")

    def test_get_post_list_view_context(self):
        self.client.force_login(self.staff_user)

        response = self.client.get(self.url)
        table_posts = list(response.context["posts"].data)

        assert response.status_code == 200
        assert "posts" in response.context
        for post in self.posts:
            assert post in table_posts

class TestDashboardPostCreateView(TestCase):
    def setUp(self):
        self.staff_user = factories.UserFactory(is_staff=True)
        self.category = factories.CategoryFactory()
        self.url = reverse("dashboard_blogs:post-create")

    def test_get_post_create_view_context(self):
        self.client.force_login(self.staff_user)

        response = self.client.get(self.url)

        assert response.status_code == 200
        assert "form" in response.context

    def test_post_post_create_view(self):
        self.client.force_login(self.staff_user)

        data = {
            "title": "Test Post",
            "body": "Test Content",
            "status": "published",
            "category": self.category.pk,
            "tags": [],
        }


        response = self.client.post(self.url, data=data)

        assert response.status_code == 302
        assert Post.objects.count() == 1
        assert Post.objects.first().title == "Test Post"
        assert Post.objects.first().body == "Test Content"
        assert Post.objects.first().category == self.category
        assert Post.objects.first().author == self.staff_user

class TestDashboardPostEditView(TestCase):
    def setUp(self):
        self.staff_user = factories.UserFactory(is_staff=True)
        self.category = factories.CategoryFactory()
        self.post = factories.PostFactory(author=self.staff_user, category=self.category)
        self.url = reverse("dashboard_blogs:post-edit", args=[self.post.pk])

    def test_get_post_edit_view_context(self):
        self.client.force_login(self.staff_user)

        response = self.client.get(self.url)

        assert response.status_code == 200
        assert "form" in response.context

    def test_post_post_edit_view(self):
        self.client.force_login(self.staff_user)

        data = {
            "title": "Updated Post",
            "body": "Updated Content",
            "status": "published",
            "category": self.category.pk,
            "tags": [],
        }

        response = self.client.post(self.url, data=data)

        self.post.refresh_from_db()

        assert response.status_code == 302
        assert response.url == reverse("dashboard_blogs:post-list")
        assert self.post.title == "Updated Post"
        assert self.post.body == "Updated Content"
        assert self.post.status == "published"
        assert self.post.category == self.category
        assert self.post.author == self.staff_user

class TestDashboardPostDeleteView(TestCase):
    def setUp(self):
        self.staff_user = factories.UserFactory(is_staff=True)
        self.post = factories.PostFactory(author=self.staff_user)
        self.url = reverse("dashboard_blogs:post-delete", args=[self.post.pk])

    def test_get_post_delete_view_context(self):
        self.client.force_login(self.staff_user)

        response = self.client.get(self.url)

        assert response.status_code == 200

    def test_post_post_delete_view(self):
        self.client.force_login(self.staff_user)

        response = self.client.post(self.url)

        assert response.status_code == 302
        assert response.url == reverse("dashboard_blogs:post-list")
        assert not Post.objects.filter(pk=self.post.pk).exists()


class TestDashboardCategoryListView(TestCase):
    def setUp(self):
        self.staff_user = factories.UserFactory(is_staff=True)
        self.categories = [factories.CategoryFactory() for _ in range(5)]
        self.url = reverse("dashboard_blogs:category-list")

    def test_get_category_list_view_context(self):
        self.client.force_login(self.staff_user)

        response = self.client.get(self.url)
        table_categories = list(response.context["categories"].data)

        assert response.status_code == 200
        assert "categories" in response.context
        for category in self.categories:
            assert category in table_categories


class TestDashboardCategoryCreateView(TestCase):
    def setUp(self):
        self.staff_user = factories.UserFactory(is_staff=True)
        self.url = reverse("dashboard_blogs:category-create")

    def test_get_category_create_view_context(self):
        self.client.force_login(self.staff_user)

        response = self.client.get(self.url)

        assert response.status_code == 200
        assert "form" in response.context

    def test_post_category_create_view(self):
        self.client.force_login(self.staff_user)

        response = self.client.post(self.url, data={"name": "Django"})

        assert response.status_code == 302
        assert response.url == reverse("dashboard_blogs:category-list")
        assert Category.objects.count() == 1
        assert Category.objects.first().name == "Django"


class TestDashboardCategoryEditView(TestCase):
    def setUp(self):
        self.staff_user = factories.UserFactory(is_staff=True)
        self.category = factories.CategoryFactory(name="Django")
        self.url = reverse("dashboard_blogs:category-edit", args=[self.category.pk])

    def test_get_category_edit_view_context(self):
        self.client.force_login(self.staff_user)

        response = self.client.get(self.url)

        assert response.status_code == 200
        assert "form" in response.context

    def test_post_category_edit_view(self):
        self.client.force_login(self.staff_user)

        response = self.client.post(self.url, data={"name": "Python"})

        self.category.refresh_from_db()

        assert response.status_code == 302
        assert response.url == reverse("dashboard_blogs:category-list")
        assert self.category.name == "Python"


class TestDashboardCategoryDeleteView(TestCase):
    def setUp(self):
        self.staff_user = factories.UserFactory(is_staff=True)
        self.category = factories.CategoryFactory()
        self.url = reverse("dashboard_blogs:category-delete", args=[self.category.pk])

    def test_get_category_delete_view_context(self):
        self.client.force_login(self.staff_user)

        response = self.client.get(self.url)

        assert response.status_code == 200

    def test_post_category_delete_view(self):
        self.client.force_login(self.staff_user)

        response = self.client.post(self.url)

        assert response.status_code == 302
        assert response.url == reverse("dashboard_blogs:category-list")
        assert not Category.objects.filter(pk=self.category.pk).exists()


class TestDashboardCommentListView(TestCase):
    def setUp(self):
        self.staff_user = factories.UserFactory(is_staff=True)
        self.other_user = factories.UserFactory()
        self.post = factories.PostFactory(author=self.staff_user)
        self.other_post = factories.PostFactory(author=self.other_user)
        self.comment = factories.CommentFactory(post=self.post)
        self.other_comment = factories.CommentFactory(post=self.other_post)
        self.url = reverse("dashboard_blogs:comment-list")

    def test_get_comment_list_view_context(self):
        self.client.force_login(self.staff_user)

        response = self.client.get(self.url)
        table_comments = list(response.context["comments"].data)

        assert response.status_code == 200
        assert "comments" in response.context
        assert self.comment in table_comments
        assert self.other_comment not in table_comments


class TestDashboardCommentDeleteView(TestCase):
    def setUp(self):
        self.staff_user = factories.UserFactory(is_staff=True)
        self.post = factories.PostFactory(author=self.staff_user)
        self.comment = factories.CommentFactory(post=self.post)
        self.url = reverse("dashboard_blogs:comment-delete", args=[self.comment.pk])

    def test_get_comment_delete_view_context(self):
        self.client.force_login(self.staff_user)

        response = self.client.get(self.url)

        assert response.status_code == 200

    def test_post_comment_delete_view(self):
        self.client.force_login(self.staff_user)

        response = self.client.post(self.url)

        assert response.status_code == 302
        assert response.url == reverse("dashboard_blogs:comment-list")
        assert not Comment.objects.filter(pk=self.comment.pk).exists()
