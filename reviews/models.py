from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Review(models.Model):
    ROLE_CHOICES = [
        ('guest', 'Гость'),
        ('critic', 'Ресторанный критик'),
        ('chef', 'Шеф-повар'),
        ('other', 'Другое'),
    ]
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='guest', verbose_name="Кто вы")
    role_description = models.CharField(max_length=100, blank=True, null=True, verbose_name="Уточните роль")
    rating = models.PositiveSmallIntegerField(verbose_name="Оценка", default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(verbose_name="Отзыв")
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False, verbose_name="Показать на сайте")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} — {self.rating}/5"