from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=35, verbose_name='Телефон', help_text='Введите номер телефона')
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True, help_text='Загрузите свой аватар')

    token = models.CharField(max_length=100, verbose_name='Token', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            ("can_manage_bookings", "Can manage all bookings"),
            ("can_view_all_bookings", "Can view all bookings"),
        ]

    def __str__(self):
        return self.email