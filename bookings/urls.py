from django.urls import path
from bookings import views
from bookings.apps import BookingsConfig

app_name = BookingsConfig.name

urlpatterns = [
    path("", views.BookingListView.as_view(), name="booking_list"),
    path("create/", views.BookingCreateView.as_view(), name="booking_form"),
    path("<int:pk>/", views.BookingDetailView.as_view(), name="booking_detail"),
    path("<int:pk>/update/", views.BookingUpdateView.as_view(), name="booking_form"),
    path("<int:pk>/delete/", views.BookingDeleteView.as_view(), name="booking_delete"),
    path("<int:pk>/confirm/", views.confirm_booking, name="booking_confirm"),
]