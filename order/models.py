from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from product.models import Product

class Order(models.Model):
    create_datetime = models.DateTimeField(_('create_datetime'), default = timezone.now())
    
    is_paid = models.BooleanField(_('is_paid'), default=False)
    
    discount = models.PositiveBigIntegerField(_('discount'), blank=True, null=True)
    
    def __str__(self):
        return f'id: {self.id}'
    
    def get_total_price(self):
        total = sum(item.item_total_price() for item in self.order_items.all())
        if self.discount:
            discount_price = (self.discount / 100) * total
            return (total - discount_price)
        return total
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = _('order')
        verbose_name_plural = _('orders')


class OrderItems(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', verbose_name=_('order'), on_delete=models.CASCADE)
    
    product = models.ForeignKey(Product, related_name='order_items', verbose_name=_('product'), on_delete=models.PROTECT)
    
    quantity = models.PositiveIntegerField(_('quantity'), default = 0)
    
    price = models.PositiveIntegerField(_('price'))
    
    def __str__(self):
        return f'product: {self.product.name}'
    
    def item_total_price(self):
        return self.price * self.quantity
    
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = _('orderitem')
        verbose_name_plural = _('orderitems')
