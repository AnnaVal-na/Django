from django.core.management.base import BaseCommand
from catalog.models import Product, Category
from django.db import transaction
import json
from pathlib import Path


class Command(BaseCommand):
    help = 'Очищает БД и загружает данные из фикстур'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():  # Все операции в одной транзакции
                # 1. Удаление старых данных
                self.stdout.write("Очистка базы данных...")
                Product.objects.all().delete()
                Category.objects.all().delete()
                self.stdout.write(self.style.SUCCESS("Данные удалены"))

                # 2. Загрузка новых данных
                self._load_fixtures()

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка: {str(e)}"))

    def _load_fixtures(self):
        """Загрузка данных из фикстур"""
        base_path = Path(__file__).parent.parent.parent.parent
        fixtures = [
            ('categories.json', Category),
            ('products.json', Product)
        ]

        for file_name, model in fixtures:
            path = base_path / 'catalog' / 'fixtures' / file_name
            self.stdout.write(f"Загрузка {file_name}...")

            with open(path, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
                for item in data:
                    fields = item['fields']
                    if model == Product:
                        fields['price'] = float(fields['price'])  # Конвертация цены
                    model.objects.create(id=item['pk'], **fields)

        self.stdout.write(self.style.SUCCESS("Все данные загружены!"))
