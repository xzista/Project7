from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("first_name","last_name","role","role_description","rating","comment")
        widgets = {
            "first_name": forms.TextInput(attrs={"class":"form-control"}),
            "last_name": forms.TextInput(attrs={"class":"form-control"}),
            "role": forms.Select(attrs={"class":"form-select"}),
            "role_description": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Если выбрано 'Другое'..."}),
            "rating": forms.NumberInput(attrs={"class":"form-control","min":1,"max":5}),
            "comment": forms.Textarea(attrs={"class":"form-control","rows":5}),
        }

    def clean_rating(self):
        r = self.cleaned_data.get("rating")
        if r < 1 or r > 5:
            raise forms.ValidationError("Оценка должна быть от 1 до 5")
        return r

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("role")
        description = cleaned_data.get("role_description")

        if role == 'other' and not description:
            # Если выбрано 'other', но описание пустое, добавляем ошибку
            msg = forms.ValidationError("Пожалуйста, уточните вашу роль в поле 'Уточните роль'.")
            # Ошибка будет привязана к полю role_description
            self.add_error('role_description', msg)

        return cleaned_data