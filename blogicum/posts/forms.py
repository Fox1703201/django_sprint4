from django import forms
from blog.models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "text", "image", "category", "pub_date"]
        widgets = {
            "pub_date": forms.DateTimeInput(attrs={"type": "datetime-local"})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = widgets = {
            "text": forms.Textarea(attrs={"class": "form-control", "rows": 3})
        }
