from django.contrib import admin

from tracker.models import PriceHistory, Product

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'current_price',
        'threshold_price_min',
        'threshold_price_max',
        'is_active',
        'updated_at'
    )
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'url')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = (
        'is_active',
        'threshold_price_min',
        'threshold_price_max'
    )

    fieldsets = (
        ('Основная информация', {
            'fields': ('url', 'name', 'is_active')
        }),
        ('Цены', {
            'fields': ('current_price', 'threshold_price_min', 'threshold_price_max')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse')
        })
    )

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