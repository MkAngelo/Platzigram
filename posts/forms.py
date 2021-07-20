"""Post forms."""

# Django import forms
from django import forms
from django.forms.models import model_to_dict

# Models
from posts.models import Post


class PostForm(forms.ModelForm):
    """Post model form."""

    class Meta:
        """Form settings."""

        model = Post
        fields = ('user','profile','title','photo')