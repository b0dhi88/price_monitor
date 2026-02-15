import asyncio
from tracker.models import PriceHistory, Product
from tracker.parsers.regard_parser import RegardParser
from celery import shared_task

@shared_task
def check_product_price(product_id):
    try:
        product = Product.objects.get(id=product_id, is_active=True)
    except Product.DoesNotExist:
        return f'Товар {product_id} не найден или неактивен'
    
    async def _parse():
        async with RegardParser(headless=True) as parser:
            return await parser.parse(product.url)
    
    result = asyncio.run(_parse())
    if result.error:
        return f'Ошибка парсинга {product_id}: {result.error}'
    
    PriceHistory.objects.create(
        product=product,
        price=result.price
    )

    product.last_price = result.price
    if not product.name:
        product.name = result.product_name or f'Товар {product_id}'
    product.save()

    if product.threshold_price_min and product.last_price <= product.threshold_price_min:
        return f'Цена упала! {product.name}: {product.last_price} <= {product.threshold_price_min}'
    if product.threshold_price_max and product.last_price >= product.threshold_price_max:
        return f'Цена выросла! {product.name}: {product.last_price} >= {product.threshold_price_max}'
    
    return f'{product.name}: {result.price}'

@shared_task
def check_all_products():
    products = Product.objects.filter(is_active=True)
    for product in products:
        check_product_price.delay(product.id)
    return f'Запущено задач: {products.count()}'