from django.core.management.base import BaseCommand
from catalog.models import Product, Category
from django.db import transaction
import json
from pathlib import Path

class Command(BaseCommand):
    help = 'Загружает категории и продукты с проверкой связей'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                self._clear_data()
                self._load_categories()
                self._load_products()
                self._validate_relations()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка: {e}"))

    def _clear_data(self):
        """Очистка старых данных"""
        self.stdout.write("🔄 Очистка старых данных...")
        Product.objects.all().delete()
        Category.objects.all().delete()

    def _load_categories(self):
        """Загрузка категорий"""
        path = Path(__file__).parent.parent.parent.parent / 'catalog' / 'fixtures' / 'categories.json'
        self.stdout.write(f"📂 Загрузка категорий из {path}")

        with open(path, 'r', encoding='utf-8-sig') as f:
            for item in json.load(f):
                Category.objects.create(
                    id=item['pk'],
                    name=item['fields']['name'],
                    description=item['fields'].get('description', '')
                )
        self.stdout.write(self.style.SUCCESS(f"✅ Загружено {Category.objects.count()} категорий"))

    def _load_products(self):
        """Загрузка продуктов с проверкой категорий"""
        path = Path(__file__).parent.parent.parent.parent / 'catalog' / 'fixtures' / 'products.json'
        self.stdout.write(f"📂 Загрузка продуктов из {path}")

        with open(path, 'r', encoding='utf-8-sig') as f:
            for item in json.load(f):
                category_id = item['fields']['category']
                if not Category.objects.filter(id=category_id).exists():
                    raise ValueError(f"Категория {category_id} не существует")

                Product.objects.create(
                    id=item['pk'],
                    name=item['fields']['name'],
                    price=float(item['fields']['price']),
                    category_id=category_id,
                    description=item['fields'].get('description', '')
                )
        self.stdout.write(self.style.SUCCESS(f"✅ Загружено {Product.objects.count()} продуктов"))

    def _validate_relations(self):
        """Проверка целостности связей"""
        orphaned = Product.objects.filter(category__isnull=True).count()
        if orphaned > 0:
            raise ValueError(f"Найдено {orphaned} продуктов без категории")
        self.stdout.write(self.style.SUCCESS("🔗 Все связи проверены"))
