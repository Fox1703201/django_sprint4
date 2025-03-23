from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.index, name="index"),
    path("category/<slug:slug>/", views.category_posts, name="category_posts"),
]
