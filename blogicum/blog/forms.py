from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "text",
            "image",
            "category",
            "pub_date",
        ]
        widgets = {
            "pub_date": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
        }
