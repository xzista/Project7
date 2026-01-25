from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "role", "rating", "is_published", "created_at")
    list_filter = ("role", "rating", "is_published")
    search_fields = ("first_name", "last_name", "comment")
    actions = ["make_published", "make_unpublished"]

    def make_published(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f"{updated} отзыв(ов) опубликовано.")
    make_published.short_description = "Опубликовать выбранные отзывы"

    def make_unpublished(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f"{updated} отзыв(ов) снято с публикации.")
    make_unpublished.short_description = "Снять публикацию"