from django.forms import TextInput, Textarea
from django.test import TestCase

from newhire.blog.forms import CommentForm, PostFilterForm
from newhire.blog.models import Comment


class TestPostFilterForm(TestCase):
    def setUp(self):
        self.form = PostFilterForm

    def test_q_field_is_optional(self):
        form = PostFilterForm(data={})

        assert form.is_valid()
        assert form.cleaned_data["q"] == ""

    def test_q_field_accepts_search_query(self):
        form = PostFilterForm(data={"q": "django"})

        assert form.is_valid()
        assert form.cleaned_data["q"] == "django"

    def test_q_field_rejects_more_than_100_characters(self):
        form = PostFilterForm(data={"q": "a" * 101})

        assert not form.is_valid()
        assert "q" in form.errors

    def test_q_field_widget_attrs(self):
        form = self.form(data={})
        field = form.fields["q"]

        assert field.label == "Search"
        assert field.required is False
        assert field.max_length == 100
        assert isinstance(field.widget, TextInput)
        assert field.widget.attrs["class"] == "form-control mr-sm-2"
        assert field.widget.attrs["placeholder"] == "Search..."


class TestCommentForm(TestCase):
    def setUp(self):
        self.form = CommentForm

    def test_body_field_is_optional(self):
        form = self.form(data={})

        assert form.is_valid()
        assert form.cleaned_data["body"] == ""

    def test_body_field_accepts_comment_text(self):
        form = self.form(data={"body": "Nice post!"})

        assert form.is_valid()
        assert form.cleaned_data["body"] == "Nice post!"

    def test_body_field_widget_attrs(self):
        form = self.form(data={})
        field = form.fields["body"]

        assert field.label == "Comment"
        assert field.required is False
        assert isinstance(field.widget, Textarea)
        assert field.widget.attrs["class"] == "wysiwyg"
        assert field.widget.attrs["rows"] == 4
        assert field.widget.attrs["placeholder"] == "Write your comment here..."

    def test_form_saves_comment_instance_without_commit(self):
        form = self.form(data={"body": "Nice post!"})
        comment = form.save(commit=False)

        assert isinstance(comment, Comment)
        assert comment.pk is None
        assert comment.body == "Nice post!"

    def test_form_uses_comment_model_and_body_field(self):
        assert self.form._meta.model == Comment
        assert self.form._meta.fields == ["body"]
