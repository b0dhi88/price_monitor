from celery import current_app
from django.contrib import admin
from django.db import transaction

from tracker.models import PriceHistory, Product

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name_display',
        'last_price',
        'threshold_price_min',
        'threshold_price_max',
        'is_active',
        'updated_at',
        'status'
    )
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'url')
    readonly_fields = ('name', 'created_at', 'updated_at')
    list_editable = (
        'is_active',
        'threshold_price_min',
        'threshold_price_max'
    )

    def name_display(self, obj):
        if obj.name:
           return obj.name
        return f'ID:{obj.id} (ожидает парсинга)'
    name_display.short_description = 'Название'

    def status(self, obj):
        if not obj.name:
            return 'Ожидает первого парсинга'
        if obj.last_price:
            if obj.threshold_price_min and obj.last_price <= obj.threshold_price_min:
                return 'Цена ниже минимального порога'
            if obj.threshold_price_max and obj.last_price >= obj.threshold_price_max:
                return 'Цена выше максимального порога'
        return 'Отслеживается'
    status.short_description = 'Статус'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change or 'url' in form.changed_data:
            transaction.on_commit(lambda: current_app.send_task(
                'tracker.tasks.check_product_price', args=[obj.id]
            ))
        
        

@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'price', 'created_at')
    list_filter = ('product', 'created_at')
    search_fields = ('product__name',)
    readonly_fields = ('product', 'price', 'created_at')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False