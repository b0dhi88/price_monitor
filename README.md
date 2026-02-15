# Price Monitor

Демо-проект: Django-приложение для мониторинга цен с парсингом через Playwright и фоновая обработка задач через Celery.

## Стек

- Python 3.11 / Django 5.x
- Playwright (парсинг)
- Celery + Redis (фоновые задачи)
- PostgreSQL (опционально)
- Docker (опционально)

## Возможности

- Модели Product и PriceHistory для хранения товаров и истории цен
- Система пороговых цен (min/max) с уведомлением
- Админ-панель для управления товарами
- Парсер для сайта regard.ru
- Базовая архитектура парсеров (можно добавлять новые)

## Статус

- [x] Django-проект с моделями
- [x] Админ-панель
- [x] Базовый парсер + RegardParser
- [~] Celery-интеграция (почти готово)
- [~] Ротация User-Agent (в процессе)
- [ ] Docker-контейнеризация
- [ ] Переход на PostgreSQL

## Установка

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install
python manage.py migrate
python manage.py runserver
```

## Запуск Celery

```bash
celery -A price_monitor worker -l info
```
