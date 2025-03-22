from django.contrib import admin

from .models import Post, Category, Location


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category", "pub_date", "is_published"]
    search_fields = ["title", "text", "author__username"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "is_published", "created_at"]
    search_fields = ["title", "slug"]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["name", "is_published", "created_at"]
    search_fields = ["name"]
