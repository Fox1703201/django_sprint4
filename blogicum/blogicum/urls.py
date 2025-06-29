from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.urls import include, path, reverse_lazy
from django.views.generic.edit import CreateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
    path("posts/", include("posts.urls", namespace="posts")),
    path("pages/", include("pages.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path(
        "auth/registration/",
        CreateView.as_view(
            template_name="registration/registration_form.html",
            form_class=UserCreationForm,
            success_url=reverse_lazy("blog:index"),
        ),
        name="registration",
    ),
    path("profile/", include("users.urls", namespace="users")),
]

handler404 = "pages.views.error_404"
handler405 = "pages.views.error_405"
handler500 = "pages.views.error_500"

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
