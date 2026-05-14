from django.test import TestCase
from django.urls import reverse


from newhire.factory.blogs import (
    UserFactory, 
    PostFactory, 
    CategoryFactory,
    TagFactory
)

class TestPostListView(TestCase):
    PAGE_SIZE = 10

    def setUp(self):
        self.user = UserFactory()
        self.posts = [PostFactory(author=self.user) for _ in range(25)]
        self.post_1 = PostFactory(author=self.user)
        self.post_2 = PostFactory()
        self.url = reverse("blogs:post-list")

    def test_get_post_list(self):
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert self.post_1.title in response.content.decode()
        assert self.post_2.title in response.content.decode()

    def test_post_list_pagination(self):
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert len(response.context["posts"]) == self.PAGE_SIZE
        assert response.context["page_obj"].number == 1

    def test_first_page_returns_200(self):
        response = self.client.get(self.url)

        assert response.status_code == 200

    def test_second_page_returns_200(self):
        response = self.client.get(self.url + "?page=2")

        assert response.status_code == 200
        assert len(response.context["posts"]) == self.PAGE_SIZE
        assert response.context["page_obj"].number == 2

    def test_post_list_search_by_title(self):
        matching_post = PostFactory(title="Django Search Result")
        other_post = PostFactory(title="Python Article")

        response = self.client.get(self.url + "?q=django")

        assert response.status_code == 200
        assert matching_post in response.context["posts"]
        assert other_post not in response.context["posts"]
    
    def test_post_list_search_by_body(self):
        matching_post = PostFactory(body="Django Search Result")
        PostFactory(body="Python Article")

        response = self.client.get(self.url + "?q=django")

        assert response.status_code == 200
        assert matching_post in response.context["posts"]
        assert "Python Article" not in response.context["posts"]

    def test_post_list_search_by_author(self):
        matching_post = PostFactory(author__name="Django Author")
        PostFactory(author__name="Python Author")

        response = self.client.get(self.url + "?q=django")

        assert response.status_code == 200
        assert matching_post in response.context["posts"]
        assert "Python Article" not in response.context["posts"]


class TestCategoryPostListView(TestCase):
    def setUp(self):
        self.category = CategoryFactory(name="Django")
        self.other_category = CategoryFactory(name="Python")
        self.post = PostFactory(category=self.category, title="Django Post")
        self.other_post = PostFactory(category=self.other_category, title="Python Post")
        self.url = reverse("blogs:post-category", args=[self.category.slug])

    def test_get_category_post_list(self):
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert self.post in response.context["posts"]
        assert self.other_post not in response.context["posts"]
        assert response.context["selected_category_slug"] == self.category.slug

    def test_get_category_post_list_with_invalid_category(self):
        url = reverse("blogs:post-category", args=["invalid-category"])
        response = self.client.get(url)

        assert response.status_code == 404

    def test_category_post_list_search_by_title(self):
        matching_post = PostFactory(category=self.category, title="Django Search Result")
        PostFactory(category=self.category, title="Python Article")

        response = self.client.get(self.url + "?q=django")

        assert response.status_code == 200
        assert matching_post in response.context["posts"]
        assert "Python Article" not in response.context["posts"]

class TestTagPostListView(TestCase):
    def setUp(self):
        self.tag = TagFactory(name="Django")
        self.other_tag = TagFactory(name="Python")
        self.post = PostFactory(title="Django Post")
        self.post.tags.add(self.tag)
        self.other_post = PostFactory(title="Python Post")
        self.other_post.tags.add(self.other_tag)
        self.url = reverse("blogs:post-tag", args=[self.tag.slug])

    def test_get_tag_post_list(self):
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert self.post in response.context["posts"]
        assert self.other_post not in response.context["posts"]
        assert response.context["selected_tag_slug"] == self.tag.slug

    def test_get_tag_post_list_with_invalid_tag(self):
        url = reverse("blogs:post-tag", args=["invalid-tag"])
        response = self.client.get(url)

        assert response.status_code == 404

    def test_tag_post_list_search_by_title(self):
        matching_post = PostFactory(title="Django Search Result")
        matching_post.tags.add(self.tag)
        PostFactory(title="Python Article")

        response = self.client.get(self.url + "?q=django")

        assert response.status_code == 200
        assert matching_post in response.context["posts"]
        assert "Python Article" not in response.context["posts"]

