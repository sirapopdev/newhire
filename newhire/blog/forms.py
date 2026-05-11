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