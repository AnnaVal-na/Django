from django.contrib import admin
from catalog.models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Поля для отображения в списке
    search_fields = ('name', 'description')  # Поля для поиска


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')  # Поля в списке
    list_filter = ('category',)  # Фильтрация по категории
    search_fields = ('name', 'description')  # Поиск по названию и описанию

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ('category', 'price')