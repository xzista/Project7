from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.dateparse import parse_date
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from .forms import BookingForm, BookingUpdateForm
from .models import Booking, RestaurantTable


# Миксин для проверки прав администратора ресторана
class RestaurantAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='RestaurantAdmins').exists() or self.request.user.is_staff

class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = "bookings/booking_list.html"
    context_object_name = "bookings"
    paginate_by = 10

    def get_queryset(self):
        qs = Booking.objects.select_related("table", "user")
        user = self.request.user

        if user.is_staff or user.groups.filter(name='RestaurantAdmins').exists():
            qs = qs.order_by("-date", "-time")
            # фильтры из GET
            q_email = self.request.GET.get("email")
            q_phone = self.request.GET.get("phone")
            q_table = self.request.GET.get("table")
            q_status = self.request.GET.get("status")
            q_date = self.request.GET.get("date")

            if q_email:
                qs = qs.filter(user__email__icontains=q_email)
            if q_phone:
                qs = qs.filter(user__phone__icontains=q_phone)
            if q_table:
                qs = qs.filter(table__name__icontains=q_table)
            if q_status:
                qs = qs.filter(status=q_status)
            if q_date:
                qs = qs.filter(date=q_date)

            # сортировка (по параметру ?order=field or -field)
            order = self.request.GET.get("order")
            if order:
                qs = qs.order_by(order)
            return qs
        else:
            return qs.filter(user=user).order_by("-date", "-time")


class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    template_name = "bookings/booking_form.html"
    form_class = BookingForm
    success_url = reverse_lazy("bookings:booking_list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Просто показываем все доступные столы
        # Валидация конфликтов будет в форме
        form.fields["table"].queryset = RestaurantTable.objects.filter(
            is_available=True
        ).order_by("capacity", "name")

        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = Booking.STATUS_CREATED

        response = super().form_valid(form)
        messages.success(self.request, "Бронирование успешно создано!")
        return response


class BookingUpdateView(LoginRequiredMixin, UpdateView):
    model = Booking
    template_name = "bookings/booking_form.html"
    form_class = BookingUpdateForm
    success_url = reverse_lazy("bookings:booking_list")

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Просто показываем все доступные столы
        # Валидация конфликтов будет в форме
        form.fields["table"].queryset = RestaurantTable.objects.filter(
            is_available=True
        ).order_by("capacity", "name")

        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = Booking.STATUS_CREATED

        response = super().form_valid(form)
        messages.success(self.request, "Бронирование успешно создано!")
        return response


class BookingDeleteView(LoginRequiredMixin, DeleteView):
    model = Booking
    template_name = "bookings/booking_confirm_delete.html"
    success_url = reverse_lazy("bookings:booking_list")

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not (self.request.user.is_staff or self.object.user == self.request.user):
            messages.error(self.request, "У вас нет прав для отмены этого бронирования.")
            return redirect(self.success_url)

        if not self.object.can_be_cancelled and not request.user.is_staff:
            messages.error(self.request, "Это бронирование нельзя отменить.")
            return redirect(self.success_url)

        self.object.status = Booking.STATUS_CANCELLED
        self.object.save()
        messages.success(self.request, "Бронирование успешно отменено!")
        return redirect(self.success_url)


class BookingDetailView(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = "bookings/booking_detail.html"
    context_object_name = "booking"

    def get_queryset(self):
        qs = super().get_queryset().select_related("table", "user")
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)


def confirm_booking(request, pk):
    """Подтверждение бронирования (только для staff)"""
    if not request.user.is_staff:
        messages.error(request, "У вас нет прав для этого действия.")
        return redirect("bookings:booking_list")

    booking = get_object_or_404(Booking, pk=pk)
    booking.status = Booking.STATUS_CONFIRMED
    booking.save()
    messages.success(request, "Бронирование подтверждено!")
    return redirect("bookings:booking_list")