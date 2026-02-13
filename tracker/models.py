from django.db import models

class Product(models.Model):
    url = models.URLField(unique=True, verbose_name='URL товара')
    name = models.CharField(max_length=255, verbose_name='Название')

    current_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Текущая цена'
    )
    threshold_price_min = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True,
        verbose_name='Мин. порог',
        help_text='Минимальная пороговая цена'
    )
    threshold_price_max = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True,
        verbose_name='Макс. порог',
        help_text='Максимальная пороговая цена'
    )

    is_active = models.BooleanField(default=True, verbose_name='Активен', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def is_threshold_reached(self):
        """Достигла ли цена границ диапазона"""
        if self.current_price is None:
            return False
        if self.threshold_price_min and self.current_price <= self.threshold_price_min:
            return True
        if self.threshold_price_max and self.current_price >= self.threshold_price_max:
            return True

class PriceHistory(models.Model):
    product=models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='price_history',
        verbose_name='Товар',
        db_index=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время проверки')

    class Meta:
        verbose_name = 'История цены'
        verbose_name_plural = 'История цен'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.product.name} - {self.price} ({self.created_at})'