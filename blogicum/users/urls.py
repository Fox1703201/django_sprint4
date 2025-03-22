from django.urls import path
from .views import ProfileView, ProfileEditView
from django.contrib.auth.views import PasswordChangeView

app_name = "users"

urlpatterns = [
    path("edit_profile/", ProfileEditView.as_view(), name="edit_profile"),
    path(
        "password_change/",
        PasswordChangeView.as_view(
            template_name="registration/password_change_form.html"
        ),
        name="password_change",
    ),
    path("<str:username>/", ProfileView.as_view(), name="profile"),
]
