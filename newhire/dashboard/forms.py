from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from newhire.blog.models import Post

MAX_FEATURED_IMAGE_SIZE = 5 * 1024 * 1024
ALLOWED_FEATURED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}


class PostSearchForm(forms.Form):
    q = forms.CharField(label="Search", required=False)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            "title",
            "body",
            "featured_image",
            "status",
            "category",
            "tags",
        )
        widgets = {
            "body": forms.Textarea(attrs={"class": "wysiwyg", "rows": 16}),
            "status": forms.RadioSelect,
            "tags": forms.SelectMultiple(attrs={"class": "select2"}),
        }

    def clean_featured_image(self):
        image = self.cleaned_data.get("featured_image")

        if not image or not hasattr(image, "content_type"):
            return image

        if image.content_type not in ALLOWED_FEATURED_IMAGE_TYPES:
            raise ValidationError(
                _("Upload a JPEG, PNG, or WebP image."),
                code="invalid_image_type",
            )

        if image.size > MAX_FEATURED_IMAGE_SIZE:
            raise ValidationError(
                _("Featured image must be 5 MB or smaller."),
                code="image_too_large",
            )

        return image
