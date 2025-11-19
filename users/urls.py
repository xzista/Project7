from django.contrib.auth.views import (LogoutView, PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path

from users.views import (ProfileUpdateView, email_verification, login_view,
                         register_view)

app_name = "users"

urlpatterns = [
    path("login/", login_view, name="login"),  # Используем нашу кастомную view
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
    path("register/", register_view, name="register"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path("profile/", ProfileUpdateView.as_view(), name="profile"),
    # --- Password reset ---
    path(
        "password-reset/",
        PasswordResetView.as_view(
            template_name="users/password_reset.html",
            email_template_name="users/password_reset_email.html",
            subject_template_name="users/password_reset_subject.txt",
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
        name="password_reset_complete",
    ),
]
