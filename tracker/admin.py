from django.contrib import admin

from tracker.models import PriceHistory, Product

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name_display',
        'current_price',
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
        if obj.current_price:
            if obj.threshold_price_min and obj.current_price <= obj.threshold_price_min:
                return 'Цена ниже минимального порога'
            if obj.threshold_price_max and obj.current_price >= obj.threshold_price_max:
                return 'Цена выше максимаьного порога'
        return 'Отслеживается'
    status.short_description = 'Статус'
        
        

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