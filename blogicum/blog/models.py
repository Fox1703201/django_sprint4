from django.contrib.auth import get_user_model
from django.db import models

from core.models import PublishedModel

User = get_user_model()


class Post(PublishedModel):
    title = models.CharField(max_length=256, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    pub_date = models.DateTimeField(
        verbose_name="Дата и время публикации",
        help_text=(
            "Если установить дату и время в будущем"
            " — можно делать отложенные публикации."
        ),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор публикации",
        related_name="posts",
    )
    location = models.ForeignKey(
        "Location",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Местоположение",
        related_name="posts",
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        related_name="posts",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Добавлено"
    )

    image = models.ImageField(
        verbose_name="Изображение",
        upload_to="posts",
        blank=True,
    )

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"

    def __str__(self):
        return self.title


class Category(PublishedModel):
    title = models.CharField(max_length=256, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    slug = models.SlugField(
        unique=True,
        verbose_name="Идентификатор",
        help_text=(
            "Идентификатор страницы для URL; "
            "разрешены символы латиницы, "
            "цифры, дефис и подчёркивание."
        ),
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Добавлено"
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title


class Location(PublishedModel):
    name = models.CharField(max_length=256, verbose_name="Название места")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Добавлено"
    )

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Публикация",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    text = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Добавлено"
    )

    class Meta:
        ordering = ["created_at"]
        verbose_name = "комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f"Коммент {self.author} к посту {self.post}"
