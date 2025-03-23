from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from blog.models import Post


class ProfileView(DetailView):
    model = User
    template_name = "blog/profile.html"
    context_object_name = "profile"

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs["username"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.get_object()

        posts = Post.objects.filter(author=user_profile).order_by(
            "-created_at"
        )

        if self.request.user == user_profile:
            posts = (
                Post.objects.filter(author=user_profile)
                .annotate(comment_count=Count("comments"))
                .order_by("-pub_date")
            )
        else:
            posts = (
                Post.objects.filter(author=user_profile, is_published=True)
                .annotate(comment_count=Count("comments"))
                .order_by("-pub_date")
            )

        paginator = Paginator(posts, 10)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context["page_obj"] = page_obj

        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["first_name", "last_name", "username", "email"]
    template_name = "blog/user.html"

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            "users:profile", kwargs={"username": self.request.user.username}
        )
