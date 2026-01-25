from datetime import date, timedelta

from django import forms

from .models import Booking


class BookingForm(forms.ModelForm):
    # Создаем кастомное поле для времени с выбором из списка
    time = forms.ChoiceField(choices=[], widget=forms.Select(attrs={"class": "form-control"}), label="Время начала")

    class Meta:
        model = Booking
        fields = ["table", "date", "time", "duration_hours", "number_of_guests", "special_requests"]
        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                    "min": date.today().isoformat(),
                    "max": (date.today() + timedelta(days=90)).isoformat(),
                }
            ),
            "duration_hours": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "number_of_guests": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "max": 20,
                }
            ),
            "special_requests": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Особые пожелания...",
                }
            ),
            "table": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Генерируем временные слоты по 15 минут
        time_slots = self.generate_time_slots()
        self.fields["time"].choices = time_slots

        # Если это редактирование существующей брони, устанавливаем текущее время
        if self.instance and self.instance.pk and self.instance.time:
            current_time = self.instance.time.strftime("%H:%M")
            if not any(current_time == choice[0] for choice in time_slots):
                self.fields["time"].choices = (
                    [("", "--- Выберите время ---")] + [(current_time, current_time)] + time_slots[1:]
                )

    def generate_time_slots(self):
        """Генерирует временные слоты с шагом 15 минут"""
        slots = [("", "--- Выберите время ---")]

        # Часы работы
        start_hour, start_minute = 12, 0  # 12:00
        end_hour, end_minute = 23, 45  # 23:45 (последний слот)

        current_hour = start_hour
        current_minute = start_minute

        while current_hour < 24:
            time_str = f"{current_hour:02d}:{current_minute:02d}"
            slots.append((time_str, time_str))

            # Увеличиваем на 15 минут
            current_minute += 15
            if current_minute >= 60:
                current_minute = 0
                current_hour += 1

            # Прерываем если достигли конца рабочего дня
            if current_hour > end_hour or (current_hour == end_hour and current_minute > end_minute):
                break

        return slots

    def clean_time(self):
        time_val = self.cleaned_data["time"]
        # Преобразуем строку в time объект
        if time_val and ":" in time_val:
            try:
                from datetime import datetime

                return datetime.strptime(time_val, "%H:%M").time()
            except ValueError:
                raise forms.ValidationError("Неверный формат времени")
        return time_val

    def clean(self):
        cleaned_data = super().clean()
        table = cleaned_data.get("table")
        date_val = cleaned_data.get("date")
        time_val = cleaned_data.get("time")
        duration_hours = cleaned_data.get("duration_hours")
        number_of_guests = cleaned_data.get("number_of_guests")

        # Проверка вместимости стола
        if table and number_of_guests and number_of_guests > table.capacity:
            raise forms.ValidationError(f"Выбранный стол вмещает максимум {table.capacity} гостей.")

        # Проверка доступности стола
        if table and date_val and time_val and duration_hours:
            from datetime import datetime, timedelta

            new_start = datetime.combine(date_val, time_val)
            new_end = new_start + timedelta(hours=duration_hours)

            # Ищем конфликтующие брони
            conflicting_bookings = Booking.objects.filter(
                table=table, date=date_val, status__in=[Booking.STATUS_CREATED, Booking.STATUS_CONFIRMED]
            ).exclude(pk=self.instance.pk if self.instance else None)

            for existing in conflicting_bookings:
                existing_start = datetime.combine(existing.date, existing.time)
                existing_end = existing_start + timedelta(hours=existing.duration_hours)

                if not (new_end <= existing_start or new_start >= existing_end):
                    raise forms.ValidationError(
                        f"Стол '{table.name}' уже забронирован на это время. "
                        f"Пожалуйста, выберите другое время или другой стол."
                    )

        return cleaned_data


class BookingUpdateForm(BookingForm):
    """Форма для обновления бронирования"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            current_time = self.instance.time.strftime("%H:%M")
            self.fields["time"].choices = [(current_time, current_time)]
