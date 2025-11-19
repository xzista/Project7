from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import timedelta, datetime

class RestaurantTable(models.Model):
    TABLE_TYPES = [
        ('2-seater', '2-местный столик'),
        ('4-seater', '4-местный столик'),
        ('6-seater', '6-местный столик'),
        ('8-seater', '8-местный столик'),
    ]

    TABLE_LOCATIONS = [
        ('hall', 'Зал'),
        ('terrace', 'Терраса'),
    ]

    name = models.CharField(max_length=50, unique=True, verbose_name="Название стола")
    table_type = models.CharField(max_length=20, choices=TABLE_TYPES, verbose_name="Тип стола")
    capacity = models.PositiveIntegerField(verbose_name="Вместимость")
    location = models.CharField(max_length=20, choices=TABLE_LOCATIONS, default='hall', verbose_name="Зона")
    is_available = models.BooleanField(default=True, verbose_name="Доступен")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    def __str__(self):
        return f"{self.name} ({self.table_type})"

class Booking(models.Model):
    STATUS_CREATED = "Создано"
    STATUS_CONFIRMED = "Подтверждено"
    STATUS_CANCELLED = "Отменено"
    STATUS_COMPLETED = "Завершено"

    STATUS_CHOICES = [
        (STATUS_CREATED, "Создано"),
        (STATUS_CONFIRMED, "Подтверждено"),
        (STATUS_CANCELLED, "Отменено"),
        (STATUS_COMPLETED, "Завершено"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings", verbose_name="Пользователь")
    table = models.ForeignKey(RestaurantTable, on_delete=models.CASCADE, verbose_name="Стол")
    date = models.DateField(verbose_name="Дата")
    time = models.TimeField(verbose_name="Время")
    duration_hours = models.PositiveIntegerField(default=2, validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="Продолжительность (часы)")
    number_of_guests = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)], verbose_name="Количество гостей")
    special_requests = models.TextField(blank=True, null=True, verbose_name="Особые пожелания")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CREATED, verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ["-date", "-time"]

    def __str__(self):
        return f"{self.user.email} - {self.table.name} - {self.date} {self.time}"

    @property
    def start_datetime(self):
        return datetime.combine(self.date, self.time)

    @property
    def end_datetime(self):
        return datetime.combine(self.date, self.time) + timedelta(hours=self.duration_hours)

    def overlaps(self, other):
        """Проверка пересечения временных интервалов с другим бронированием"""
        return not (self.end_datetime <= other.start_datetime or self.start_datetime >= other.end_datetime)

    @property
    def is_past_due(self):
        booking_datetime = timezone.make_aware(timezone.datetime.combine(self.date, self.time))
        return timezone.now() > booking_datetime

    @property
    def can_be_modified(self):
        return self.status in [self.STATUS_CREATED, self.STATUS_CONFIRMED] and not self.is_past_due

    @property
    def can_be_cancelled(self):
        return self.status in [self.STATUS_CREATED, self.STATUS_CONFIRMED] and not self.is_past_due