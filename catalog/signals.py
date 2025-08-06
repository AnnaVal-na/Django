from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product, Category

@receiver([post_save, post_delete], sender=Product)
def invalidate_product_cache(sender, instance, **kwargs):
    """Инвалидация кеша при изменении продуктов"""
    cache.delete('all_products')  # Весь список продуктов
    if instance.category:
        cache.delete(f'products_category_{instance.category.id}')  # Кеш категории
    cache.delete(f'product_{instance.id}')  # Детальная страница продукта

@receiver([post_save, post_delete], sender=Category)
def invalidate_category_cache(sender, instance, **kwargs):
    """Инвалидация кеша при изменении категорий"""
    cache.delete('all_products')
    cache.delete(f'products_category_{instance.id}')
