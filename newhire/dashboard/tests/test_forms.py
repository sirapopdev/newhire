from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from newhire.dashboard.forms import CategoryForm
from newhire.dashboard.forms import MAX_FEATURED_IMAGE_SIZE
from newhire.dashboard.forms import PostForm
from newhire.factory.blogs import CategoryFactory
from newhire.factory.blogs import TagFactory

NO_IMAGE_PATH = Path("newhire/static/images/no-image.png")


class TestPostForm(TestCase):
    def setUp(self):
        self.category = CategoryFactory()
        self.tag = TagFactory()
        self.form_data = {
            "title": "Test Post",
            "body": "Test Content",
            "status": "published",
            "category": self.category.pk,
            "tags": [self.tag.pk],
        }

    def test_post_form_is_valid(self):
        form = PostForm(data=self.form_data)

        assert form.is_valid()

    def test_post_form_fields(self):
        form = PostForm()

        assert list(form.fields) == [
            "title",
            "body",
            "featured_image",
            "status",
            "category",
            "tags",
        ]

    def test_post_form_widgets(self):
        form = PostForm()

        assert form.fields["body"].widget.attrs["class"] == "wysiwyg"
        assert form.fields["body"].widget.attrs["rows"] == 16
        assert form.fields["tags"].widget.attrs["class"] == "select2"

    def test_featured_image_rejects_invalid_content_type(self):
        image = SimpleUploadedFile(
            "test.txt",
            b"not an image",
            content_type="text/plain",
        )
        form = PostForm(data=self.form_data, files={"featured_image": image})

        assert not form.is_valid()
        assert "featured_image" in form.errors

    def test_featured_image_rejects_large_file(self):
        image = SimpleUploadedFile(
            "test.png",
            b"a" * (MAX_FEATURED_IMAGE_SIZE + 1),
            content_type="image/png",
        )
        form = PostForm(data=self.form_data, files={"featured_image": image})

        assert not form.is_valid()
        assert "featured_image" in form.errors

    def test_clean_featured_image_returns_none_without_image(self):
        form = PostForm(data=self.form_data)
        form.is_valid()

        assert form.clean_featured_image() is None

    def test_clean_featured_image_returns_file_without_content_type(self):
        form = PostForm(data=self.form_data)
        form.cleaned_data = {"featured_image": object()}
        image = form.cleaned_data["featured_image"]

        assert form.clean_featured_image() == image

    def test_featured_image_accepts_valid_image(self):
        image = SimpleUploadedFile(
            "test.png",
            NO_IMAGE_PATH.read_bytes(),
            content_type="image/png",
        )
        form = PostForm(data=self.form_data, files={"featured_image": image})

        assert form.is_valid()
        assert form.cleaned_data["featured_image"] == image


class TestCategoryForm(TestCase):
    def setUp(self):
        self.form_data = {"name": "Django"}

    def test_category_form_is_valid(self):
        form = CategoryForm(data=self.form_data)

        assert form.is_valid()

    def test_category_form_fields(self):
        form = CategoryForm()

        assert list(form.fields) == ["name"]
