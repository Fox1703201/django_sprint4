from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.utils.timezone import now

from blog.models import Category, Post


def index(request):
    template = "blog/index.html"
    post_list = (
        Post.objects.filter(
            is_published=True, pub_date__lte=now(), category__is_published=True
        )
        .annotate(comment_count=Count("comments"))
        .order_by("-pub_date")
    )

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}
    return render(request, template, context)


def category_posts(request, slug):
    template = "blog/category.html"
    category = get_object_or_404(Category, slug=slug, is_published=True)
    post_list = Post.objects.filter(
        category=category, is_published=True, pub_date__lte=now()
    ).order_by("-pub_date")

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"category": category, "page_obj": page_obj}
    return render(request, template, context)
