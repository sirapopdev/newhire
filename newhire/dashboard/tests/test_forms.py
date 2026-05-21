from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image

from newhire.dashboard.forms import MAX_FEATURED_IMAGE_SIZE, CategoryForm, PostForm
from newhire.test import factories


def uploaded_image(
    name="test.png",
    image_format="PNG",
    content_type="image/png",
    extra_bytes=b"",
):
    image_file = BytesIO()
    Image.new("RGB", (1, 1), color="white").save(image_file, image_format)
    return SimpleUploadedFile(
        name,
        image_file.getvalue() + extra_bytes,
        content_type=content_type,
    )


class TestPostForm(TestCase):
    def setUp(self):
        self.user = factories.UserFactory()
        self.category = factories.CategoryFactory()
        self.tag = factories.TagFactory()
        self.form = PostForm

    def test_post_form_is_valid(self):
        data = {
            "title": "Test Post",
            "body": "Test Content",
            "status": "published",
            "category": self.category.pk,
            "tags": [self.tag.pk],
        }
        form = self.form(data=data)

        assert form.is_valid()

        form.instance.author = self.user
        post = form.save()

        assert post.title == "Test Post"
        assert post.body == "Test Content"
        assert post.status == "published"
        assert post.category == self.category
        assert post.author == self.user
        assert list(post.tags.all()) == [self.tag]

    def test_post_form_fields(self):
        form = self.form(data={})

        assert list(form.fields) == [
            "title",
            "body",
            "featured_image",
            "status",
            "category",
            "tags",
        ]

    def test_post_form_widgets(self):
        form = self.form(data={})

        assert form.fields["body"].widget.attrs["class"] == "wysiwyg"
        assert form.fields["body"].widget.attrs["rows"] == 16
        assert form.fields["tags"].widget.attrs["class"] == "select2"

    def test_featured_image_rejects_invalid_content_type(self):
        image = uploaded_image(
            "test.gif",
            image_format="GIF",
            content_type="image/gif",
        )
        data = {
            "title": "Test Post",
            "body": "Test Content",
            "status": "published",
            "category": self.category.pk,
            "tags": [self.tag.pk],
        }
        form = self.form(data=data, files={"featured_image": image})

        assert not form.is_valid()
        assert "featured_image" in form.errors
        error = form.errors.as_data()["featured_image"][0]
        assert error.code == "invalid_image_type"
        assert str(error.message) == "Upload a JPEG, PNG, or WebP image."

    def test_featured_image_rejects_large_file(self):
        image = uploaded_image(
            "test.png",
            extra_bytes=b"x" * (MAX_FEATURED_IMAGE_SIZE + 1),
            content_type="image/png",
        )
        data = {
            "title": "Test Post",
            "body": "Test Content",
            "status": "published",
            "category": self.category.pk,
            "tags": [self.tag.pk],
        }
        form = self.form(data=data, files={"featured_image": image})

        assert not form.is_valid()
        assert "featured_image" in form.errors
        error = form.errors.as_data()["featured_image"][0]
        assert error.code == "image_too_large"
        assert str(error.message) == "Featured image must be 5 MB or smaller."

    def test_clean_featured_image_returns_none_without_image(self):
        data = {
            "title": "Test Post",
            "body": "Test Content",
            "status": "published",
            "category": self.category.pk,
            "tags": [self.tag.pk],
        }
        form = self.form(data=data)

        assert form.is_valid() is True
        assert form.clean_featured_image() is None

    def test_clean_featured_image_returns_file_without_content_type(self):
        data = {
            "title": "Test Post",
            "body": "Test Content",
            "status": "published",
            "category": self.category.pk,
            "tags": [self.tag.pk],
        }
        form = self.form(data=data)
        form.cleaned_data = {"featured_image": object()}
        image = form.cleaned_data["featured_image"]

        assert form.clean_featured_image() == image

    def test_featured_image_accepts_valid_image(self):
        image = uploaded_image(
            "test.png",
            content_type="image/png",
        )
        data = {
            "title": "Test Post",
            "body": "Test Content",
            "status": "published",
            "category": self.category.pk,
            "tags": [self.tag.pk],
        }
        form = self.form(data=data, files={"featured_image": image})

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
