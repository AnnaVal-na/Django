from django.db import models


class Category(models.Model):
    """Модель категории товаров"""
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)

    # Автоматически добавляемые даты
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    """Модель товара"""
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    image = models.ImageField(upload_to='products/', verbose_name='Изображение', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name='Категория', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за покупку')

    # Автоматически добавляемые даты
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name', 'price']  # Сортировка по умолчанию

class Meta:
    constraints = [
        models.UniqueConstraint(fields=['name'], name='unique_category_name')
    ]
