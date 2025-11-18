from django import forms
from datetime import date, timedelta
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["table", "date", "time", "duration_hours", "number_of_guests", "special_requests"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "duration_hours": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 4}),
            "number_of_guests": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 20}),
            "special_requests": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Особые пожелания..."}),
            "table": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Устанавливаем минимальную дату - сегодня
        self.fields["date"].widget.attrs["min"] = date.today().isoformat()
        # Максимальная дата - через 3 месяца
        max_date = date.today() + timedelta(days=90)
        self.fields["date"].widget.attrs["max"] = max_date.isoformat()

    def clean(self):
        cleaned_data = super().clean()
        table = cleaned_data.get("table")
        date_val = cleaned_data.get("date")
        time_val = cleaned_data.get("time")
        number_of_guests = cleaned_data.get("number_of_guests")

        if table and number_of_guests and number_of_guests > table.capacity:
            raise forms.ValidationError(
                f"Выбранный стол вмещает максимум {table.capacity} гостей."
            )

        if table and date_val and time_val:
            # Проверяем, не занят ли стол на это время
            conflicting_booking = Booking.objects.filter(
                table=table,
                date=date_val,
                time=time_val,
                status__in=[Booking.STATUS_CREATED, Booking.STATUS_CONFIRMED]
            ).exclude(pk=self.instance.pk if self.instance else None)

            if conflicting_booking.exists():
                raise forms.ValidationError(
                    "Этот стол уже забронирован на выбранное время. Пожалуйста, выберите другое время или стол."
                )

        return cleaned_data

class BookingUpdateForm(BookingForm):
    """Форма для обновления бронирования"""

    def clean_date(self):
        reservation_date = self.cleaned_data["date"]
        if reservation_date < date.today():
            raise forms.ValidationError("Нельзя перенести бронирование на прошедшую дату.")
        return reservation_date