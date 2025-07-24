from django import forms
from django.core.exceptions import ValidationError
from .models import Product

# Запрещенные слова для названия и описания
FORBIDDEN_WORDS = [
    "казино", "криптовалюта", "крипта", "биржа",
    "дешево", "бесплатно", "обман", "полиция", "радар"
]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']


    def clean_name(self):
        """Проверяем название на запрещенные слова"""
        name = self.cleaned_data['name'].lower()
        for word in FORBIDDEN_WORDS:
            if word in name:
                raise ValidationError(f"Название содержит запрещенное слово: '{word}'")
        return self.cleaned_data['name']


    def clean_description(self):
        """Проверяем описание на запрещенные слова"""
        description = self.cleaned_data['description'].lower()
        for word in FORBIDDEN_WORDS:
            if word in description:
                raise ValidationError(f"Описание содержит запрещенное слово: '{word}'")
        return self.cleaned_data['description']


    def clean_price(self):
        """Проверяем, что цена не отрицательная"""
        price = self.cleaned_data['price']
        if price < 0:
            raise ValidationError("Цена не может быть отрицательной!")
        return price


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Добавляем CSS-классы для всех полей
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        # Особые стили для чекбокса (если есть булево поле)
        if 'is_published' in self.fields:
            self.fields['is_published'].widget.attrs['class'] = 'form-check-input'