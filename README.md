# Price Monitor

Демо-проект: Django-приложение для мониторинга цен с парсингом через Playwright и фоновая обработка задач через Celery.

## Стек

- Python 3.11 / Django 5.x
- Playwright, httpx, BeautifulSoup4 (парсинг)
- Celery (фоновые задачи)
- Redis (брокер сообщений)
- Docker

## Технические решения

- Модели Product и PriceHistory для хранения товаров и истории цен
- Система пороговых цен (min/max) с уведомлением
- Админ-панель для управления товарами
- Реестр парсеров с валидацией URL и унифицированной обработкой результатов
- Парсеры: RegardParser, ExtraFurnituraParser
- Автоматический парсинг названия и цены при сохранении товара в админке
- Асинхронный парсинг с защитой от race conditions
- Пакетная проверка цен в одном event loop
- Улучшенная обработка ошибок в фоновых задачах

## Статус

- [x] Django-проект с моделями
- [x] Админ-панель
- [x] Парсеры (Regard, Extra-Furnitura)
- [x] Реестр парсеров с валидацией
- [x] Celery-интеграция
- [x] Redis-интеграция (авто-проверка цен)
- [ ] Ротация User-Agent
- [x] Docker-контейнеризация
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

## Запуск через Docker

```bash
docker compose up -d
```

### Команды Docker

```bash
# Пересборка после изменений
docker compose down && docker compose build --no-cache && docker compose up -d

# Логи worker
docker logs -f price_monitor-worker-1

# Запуск парсинга
docker exec price_monitor-web-1 python manage.py shell -c "from tracker.tasks import check_all_products; print(check_all_products.delay())"
```

## Доступные парсеры

- `RegardParser` - для парсинга сайта regard.ru
- `ExtraFurnituraParser` - для парсинга сайта extra-furnitura.ru
