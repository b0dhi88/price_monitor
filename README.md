# Price Monitor

Демо-проект: Django-приложение для мониторинга цен с парсингом через Playwright и фоновая обработка задач через Celery.

## Стек

- Python 3.11 / Django 5.x
- Playwright (парсинг)
- Celery (фоновые задачи)
- Redis (брокер сообщений)
- Docker (планируется)

## Технические решения

- Модели Product и PriceHistory для хранения товаров и истории цен
- Система пороговых цен (min/max) с уведомлением
- Админ-панель для управления товарами
- Парсер для сайта regard.ru
- Базовая архитектура парсеров (можно добавлять новые)
- Автоматический парсинг названия и цены при сохранении товара в админке
- Асинхронный парсинг с защитой от race conditions
- Пакетная проверка цен в одном event loop

## Статус

- [x] Django-проект с моделями
- [x] Админ-панель
- [x] Базовый парсер + RegardParser
- [x] Celery-интеграция
- [x] Redis-интеграция (авто-проверка цен)
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
