from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Удаляет старые данные и добавляет тестовые продукты и категории'

    def handle(self, *args, **options):
        # Удаляем все существующие данные
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Все старые данные удалены!'))

        # Создаем категории
        electronics = Category.objects.create(
            name="Электроника",
            description="Гаджеты и техника"
        )
        books = Category.objects.create(
            name="Книги",
            description="Художественная и учебная литература"
        )
        self.stdout.write(self.style.SUCCESS('Созданы категории'))

        # Создаем продукты
        test_products = [
            {
                "name": "Смартфон",
                "price": 29999.99,
                "category": electronics,
                "description": "Новый флагман"
            },
            {
                "name": "Ноутбук",
                "price": 79999.99,
                "category": electronics,
                "description": "Игровой ноутбук"
            },
            {
                "name": "Python для начинающих",
                "price": 1500.00,
                "category": books,
                "description": "Лучший учебник"
            }
        ]

        for product in test_products:
            Product.objects.create(**product)

        self.stdout.write(
            self.style.SUCCESS(f'Добавлено {len(test_products)} тестовых продуктов')
        )
