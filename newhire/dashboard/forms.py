from django import forms

from newhire.blog.models import Post


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
