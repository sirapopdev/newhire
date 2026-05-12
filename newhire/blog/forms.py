from django import forms
from .models import Comment


class PostFilterForm(forms.Form):
    q = forms.CharField(
        label="Search", 
        max_length=100, 
        required=False, 
        widget=forms.TextInput(attrs={
            'class': 'form-control mr-sm-2',
            'placeholder': 'Search...'
        })
    )

class CommentForm(forms.ModelForm):
    body = forms.CharField(
        label='Comment',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'wysiwyg',
            'rows': 4,
            'placeholder': 'Write your comment here...'
        })
    )
    class Meta:
        model = Comment
        fields = ['body']