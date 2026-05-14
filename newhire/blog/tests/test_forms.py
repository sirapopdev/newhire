from django.forms import TextInput, Textarea
from django.test import TestCase

from newhire.blog.forms import CommentForm, PostFilterForm
from newhire.blog.models import Comment


class TestPostFilterForm(TestCase):
    def setUp(self):
        self.empty_form = PostFilterForm(data={})
        self.search_form = PostFilterForm(data={"q": "django"})
        self.form = PostFilterForm()

    def test_q_field_is_optional(self):
        assert self.empty_form.is_valid()
        assert self.empty_form.cleaned_data["q"] == ""

    def test_q_field_accepts_search_query(self):
        assert self.search_form.is_valid()
        assert self.search_form.cleaned_data["q"] == "django"

    def test_q_field_rejects_more_than_100_characters(self):
        form = PostFilterForm(data={"q": "a" * 101})

        assert not form.is_valid()
        assert "q" in form.errors

    def test_q_field_widget_attrs(self):
        field = self.form.fields["q"]

        assert field.label == "Search"
        assert field.required is False
        assert field.max_length == 100
        assert isinstance(field.widget, TextInput)
        assert field.widget.attrs["class"] == "form-control mr-sm-2"
        assert field.widget.attrs["placeholder"] == "Search..."


class TestCommentForm(TestCase):
    def setUp(self):
        self.empty_form = CommentForm(data={})
        self.comment_form = CommentForm(data={"body": "Nice post!"})
        self.form = CommentForm()

    def test_body_field_is_optional(self):
        assert self.empty_form.is_valid()
        assert self.empty_form.cleaned_data["body"] == ""

    def test_body_field_accepts_comment_text(self):
        assert self.comment_form.is_valid()
        assert self.comment_form.cleaned_data["body"] == "Nice post!"

    def test_body_field_widget_attrs(self):
        field = self.form.fields["body"]

        assert field.label == "Comment"
        assert field.required is False
        assert isinstance(field.widget, Textarea)
        assert field.widget.attrs["class"] == "wysiwyg"
        assert field.widget.attrs["rows"] == 4
        assert field.widget.attrs["placeholder"] == "Write your comment here..."

    def test_form_saves_comment_instance_without_commit(self):
        comment = self.comment_form.save(commit=False)

        assert isinstance(comment, Comment)
        assert comment.pk is None
        assert comment.body == "Nice post!"

    def test_form_uses_comment_model_and_body_field(self):
        assert self.form._meta.model == Comment
        assert self.form._meta.fields == ["body"]
