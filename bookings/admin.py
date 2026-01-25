from django.contrib import admin

from .models import Booking, RestaurantTable


@admin.register(RestaurantTable)
class RestaurantTableAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "table_type", "capacity", "location", "is_available")
    list_filter = ("table_type", "location", "is_available")
    search_fields = ("name",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "user_email", "user_phone", "table", "date", "time", "duration_hours", "status")
    list_filter = ("status", "date", "table__location")
    search_fields = ("user__email", "user__phone", "table__name")
    actions = ["confirm_bookings", "cancel_bookings"]

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = "Email"

    def user_phone(self, obj):
        return obj.user.phone

    user_phone.short_description = "Phone"

    def confirm_bookings(self, request, queryset):
        updated = queryset.update(status=Booking.STATUS_CONFIRMED)
        self.message_user(request, f"{updated} бронирований подтверждено.")

    confirm_bookings.short_description = "Подтвердить выбранные брони"

    def cancel_bookings(self, request, queryset):
        updated = queryset.update(status=Booking.STATUS_CANCELLED)
        self.message_user(request, f"{updated} бронирований отменено.")

    cancel_bookings.short_description = "Отменить выбранные брони"
