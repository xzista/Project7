import secrets

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import UpdateView

from config.settings import EMAIL_HOST_USER, SITE_URL
from users.forms import ProfileUpdateForm, UserLoginForm, UserRegisterForm
from users.models import User


def register_view(request):
    """
    View для регистрации нового пользователя.
    """
    if request.method == "POST":
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Пользователь не активен до подтверждения email
            token = secrets.token_hex(16)
            user.token = token
            user.save()

            # Автоматически добавляем в группу Customers если она существует
            try:
                customer_group = Group.objects.get(name="Customers")
                user.groups.add(customer_group)
            except Group.DoesNotExist:
                pass

            # Отправка email для подтверждения
            url = f"{SITE_URL}/users/email-confirm/{token}"
            send_mail(
                subject="Подтверждение почты - Le Jardin Secret",
                message=f"""Добро пожаловать в Le Jardin Secret!

Для завершения регистрации и подтверждения вашего email адреса, пожалуйста, перейдите по ссылке:
{url}

С уважением,
Команда Le Jardin Secret

Это письмо отправлено автоматически, отвечать на него не нужно.""",
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
            )

            messages.success(request, "Регистрация прошла успешно! Проверьте вашу почту для подтверждения email.")
            return redirect("home")
    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", {"form": form})


def login_view(request):
    """
    Кастомная view для входа пользователя.
    """
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f"Добро пожаловать, {user.email}!")
                    next_url = request.GET.get("next", "home")
                    return redirect(next_url)
                else:
                    messages.error(
                        request, "Ваш аккаунт не активирован. Проверьте вашу почту для подтверждения email."
                    )
            else:
                messages.error(request, "Неверный email или пароль.")
    else:
        form = UserLoginForm()

    return render(request, "users/login.html", {"form": form})


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    View для обновления профиля пользователя.
    """

    model = User
    form_class = ProfileUpdateForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Профиль успешно обновлен!")
        return super().form_valid(form)


def email_verification(request, token):
    """
    View для подтверждения email.
    """
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.token = None  # Очищаем токен после использования
    user.save()

    # Автоматически логиним пользователя после подтверждения email
    login(request, user)

    messages.success(request, "Email успешно подтвержден! Добро пожаловать в Le Jardin Secret!")
    return redirect(reverse("home"))
