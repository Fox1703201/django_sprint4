from django.urls import path
from . import views
from .views import (
    PostCreateView,
    PostEditView,
    PostDeleteView,
    CommentEditView,
    CommentDeleteView,
    add_comment,
)

app_name = "posts"

urlpatterns = [
    path("<int:id>/", views.post_detail, name="post_detail"),
    path("create/", PostCreateView.as_view(), name="create_post"),
    path("<int:pk>/edit/", PostEditView.as_view(), name="edit_post"),
    path("<int:pk>/delete", PostDeleteView.as_view(), name="delete_post"),
    path("<post_id>/comment", add_comment, name="add_comment"),
    path(
        "<int:post_id>/edit_comment/<int:pk>/",
        CommentEditView.as_view(),
        name="edit_comment",
    ),
    path(
        "<int:post_id>/delete_comment/<int:pk>/",
        CommentDeleteView.as_view(),
        name="delete_comment",
    ),
]
