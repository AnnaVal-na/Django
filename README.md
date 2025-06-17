# Интернет-магазин

## Описание
Это проект интернет-магазина, который будет развиваться поэтапно на каждом уроке курса.

## Структура проекта
- `catalog`: Приложение для каталога товаров.
- `config`: Настройки Django-проекта.

## Как запустить проект
1. Клонируйте репозиторий:
   ```bash
   git clone <repository_url>
   Активируйте виртуальное окружение:
bash

source venv/Scripts/activate  # Windows
source venv/bin/activate      # macOS/Linux
Установите зависимости:
bash

pip install -r requirements.txt
Перейдите в директорию проекта:
bash

cd DjangoProject
Примените миграции:
bash

python manage.py migrate
Запустите сервер:
bash

python manage.py runserver
Ветвление
main: Главная ветка для релизов.
develop: Ветка для разработки.
hwX: Ветки для домашних заданий.