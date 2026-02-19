import asyncio
import logging
import random
from tracker.models import PriceHistory, Product
from tracker.parsers.registry import get_parser_for_url
from tracker.parsers.regard_parser import RegardParser
from celery import shared_task
from django.db import transaction

logger = logging.getLogger(__name__)


def _get_parser_for_product(product):
    parser_name = get_parser_for_url(product.url)
    if parser_name == 'ExtraFurnituraParser':
        from tracker.parsers.extra_furnitura_parser import ExtraFurnituraParser
        return ExtraFurnituraParser()
    return RegardParser(headless=True)


@shared_task
def check_product_price(product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return f'Товар {product_id} не найден'
    
    if not product.is_active:
        return f'Товар {product_id} неактивен'
    
    async def _parse(product):
        parser = _get_parser_for_product(product)
        async with parser:
            return await parser.parse(product.url)
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(_parse(product))
    finally:
        loop.close()
    
    if not _process_parsing_result(product, result):
        return f'Ошибка парсинга {product_id}: {result.error}'
    
    return f'{product.name}: {result.price}'


def _process_parsing_result(product, result):
    if result.error:
        logger.error(f'Ошибка парсинга {product.url}: {result.error}')
        return False
    
    _save_result(product, result)
    return True


@shared_task
def check_all_products():
    products = list(Product.objects.filter(is_active=True))
    if not products:
        return 'Нет активных товаров'
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        results = loop.run_until_complete(_parse_all_safe(products))
    finally:
        loop.close()
    
    success_count = sum(1 for p, r in results if _process_parsing_result(p, r))
    
    return f'Проверено {success_count}/{len(products)} товаров'


async def _parse_all_safe(products):
    results = []
    for product in products:
        parser = _get_parser_for_product(product)
        async with parser:
            result = await parser.parse(product.url)
            results.append((product, result))
            await asyncio.sleep(random.uniform(2, 5))
    return results

def _save_result(product, result):
    with transaction.atomic():
        PriceHistory.objects.create(
            product=product,
            price=result.price
        )
        product.last_price = result.price
        if not product.name:
            product.name = result.product_name or f'Товар {product.id}'
        product.save()

# def _check_trasholds(product, result):
#     if product.threshold_price_min and result.price <= product.threshold_price_min:
#         return f'Цена упала! {product.name}: {result.price} <= {product.threshold_price_min}'
#     if product.threshold_price_max and result.price >= product.threshold_price_max:
#         return f'Цена выросла! {product.name}: {result.price} >= {product.threshold_price_max}'