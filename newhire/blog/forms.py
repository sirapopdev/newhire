from django import forms


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

    category = forms.ChoiceField(
        required=False,
        choices=[],
        widget=forms.Select(attrs={
            "class": "blog-nav-filter__select form-control form-control-sm",
            "aria-label": "Category",
            "onchange": "this.form.submit()",
        }), 
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Category
        categories = Category.objects.all()
        self.fields['category'].choices = [('', 'All categories')] + [(cat.slug, cat.name) for cat in categories]