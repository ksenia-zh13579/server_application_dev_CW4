# Разработка серверных приложений - Контрольная работа №3
--

## Заполнение переменных окружения

Для установки значений нужных переменных окружения нужно создать файл ".env", скопировать туда названия переменных из файла ".env.example" и дописать соответствующие значения каждой из них. Файл ".env" нужно добавить в .gitignore.
--

## Создание виртуального окружения

В этом и последующих пунктах указанные команды следует выполнять в терминале из корневой папки.

Для создания виртуального окружения нужно выполнить следующие команды:
 - python -m venv venv
 - source venv/bin/activate  # для Linux/Mac
 - venv\Scripts\activate     # для Windows
--

## Установка зависимостей

pip install -r requirements.txt
--

## Запуск приложения
uvicorn app:app --reload
--

## Задание 9.1

Применение конкретной миграции (revision указан в начале файла миграции из папки alembic/versions):
 - alembic upgrade <revision>

Применение последней миграции:
 - alembic upgrade head

Откат к определенной версии:
 - alembic downgrade <revision>

Автоматическая генерация миграции:
 - alembic revision --autogenerate -m "описание изменений"

## Задания 10-11

### Маршруты

 - GET Product: curl http://127.0.0.1:8000/products/{product_id}
 - POST Product: curl -X POST http://127.0.0.1:8000/products/ -H "Content-Type: application/json" -d '{"title"="pencil", "price"=87, "count"=120, "description"="graphite pencil, black"}'
 - DELETE Product: curl -D http://127.0.0.1:8000/products/{product_id}

## Тестирование

 - Задания 10 - тесты: pytest tests/test_main.py
 - Задания 11 - асинхронные тесты: pytest tests/test_async.py
--

## Сведения

Работу выполнила Жужлева Ксения Александровна, группа ЭФБО-05-24.