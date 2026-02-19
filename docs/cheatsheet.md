# Price Monitor - Команды

## Запуск тасков

```bash
# Одиночный парсинг (product_id - id товара в БД)
docker exec price_monitor-web-1 python manage.py shell -c "from tracker.tasks import check_product_price; print(check_product_price.delay(1))"

# Парсинг всех активных товаров
docker exec price_monitor-web-1 python manage.py shell -c "from tracker.tasks import check_all_products; print(check_all_products.delay())"
```

## Логи

```bash
# Следить за логами worker в реальном времени
docker logs -f price_monitor-worker-1

# Последние 50 строк
docker logs price_monitor-worker-1 | tail -50
```

## Пересборка

```bash
# После изменений в коде
docker compose down && docker compose build --no-cache && docker compose up -d
```

## Контейнеры

| Контейнер | Назначение | Порт |
|-----------|------------|------|
| price_monitor-web-1 | Django | 8000 |
| price_monitor-worker-1 | Celery | - |
| price_monitor-redis-1 | Redis | 6379 |

## Важно

- URL товара определяет парсер через `tracker/parsers/registry.py`
- Нельзя хардкодить парсер в `tasks.py` - нужно использовать registry
- Добавлять новые парсеры в `PARSER_REGISTRY` в `registry.py`

## Django Admin

- URL: http://localhost:8000/admin/
- Логин: admin / admin123
