from django.contrib.auth.views import (
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import path, reverse_lazy

from users.views import ProfileUpdateView, email_verification, login_view, register_view

app_name = "users"

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
    path("register/", register_view, name="register"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path("profile/", ProfileUpdateView.as_view(), name="profile"),

    # --- Password reset ---
    # Форма запроса сброса пароля
    path(
        "password-reset/",
        PasswordResetView.as_view(
            template_name="users/password_reset.html",
            email_template_name="users/password_reset_email.txt",  # текстовое письмо
            subject_template_name="users/password_reset_subject.txt",
            success_url=reverse_lazy("users:password_reset_done"),  # редирект после отправки письма
        ),
        name="password_reset",
    ),

    # Страница подтверждения, что письмо отправлено
    path(
        "password-reset/done/",
        PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),

    # Форма установки нового пароля по ссылке из письма
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url=reverse_lazy("users:password_reset_complete"),  # редирект после смены пароля
        ),
        name="password_reset_confirm",
    ),

    # Страница подтверждения успешного сброса пароля
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]