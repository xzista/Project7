from django.db import models
from django.urls import reverse

class MenuCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Категория")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name

class Dish(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    category = models.ForeignKey(MenuCategory, on_delete=models.PROTECT, related_name="dishes", verbose_name="Категория")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена")
    description = models.TextField(blank=True, verbose_name="Описание")
    is_available = models.BooleanField(default=True, verbose_name="В наличии")
    image = models.ImageField(upload_to="menu/images/", blank=True, null=True, verbose_name="Фото")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"
        ordering = ["category__name", "name"]

    def __str__(self):
        return f"{self.name} — {self.price}₽"

    def get_absolute_url(self):
        return reverse("menu:dish_detail", args=[self.pk])