from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import CreateView, DeleteView, UpdateView

from blog.models import Comment, Post

from .forms import CommentForm, PostForm


def post_detail(request, id):
    template = "blog/detail.html"

    filters = Q(is_published=True, pub_date__lte=now()) & (
        Q(category__is_published=True) | Q(category__isnull=True)
    )

    if request.user.is_authenticated:
        filters = filters | Q(author=request.user)

    post = get_object_or_404(Post.objects.filter(filters), pk=id)

    comments = post.comments.all()
    form = CommentForm()

    context = {"post": post, "comments": comments, "form": form}
    return render(request, template, context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/create.html"

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user

        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "users:profile", kwargs={"username": self.request.user.username}
        )


class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/create.html"

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

    def handle_no_permission(self):
        return redirect("posts:post_detail", id=self.get_object().id)

    def get_success_url(self):
        return reverse_lazy("posts:post_detail", kwargs={"id": self.object.id})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/create.html"

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PostForm(instance=self.object)
        return context

    def get_success_url(self):
        return reverse_lazy(
            "users:profile", kwargs={"username": self.request.user.username}
        )


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect("posts:post_detail", id=post_id)

    return redirect("posts:post_detail", id=post_id)


class CommentEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment.html"

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy(
            "posts:post_detail", kwargs={"id": self.object.post.id}
        )


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment.html"

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy(
            "posts:post_detail", kwargs={"id": self.object.post.id}
        )
