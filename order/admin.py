# Django libraries
from django.contrib.postgres.fields import JSONField
from typing import Any
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.db.models import Count, Subquery, OuterRef
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.translation import gettext_lazy as _

# Third party libraries
from jalali_date.admin import ModelAdminJalaliMixin, TabularInlineJalaliMixin
from jalali_date import datetime2jalali, date2jalali	

# My libraries
from .models import Order, OrderItems



class OrderItemsInline(TabularInlineJalaliMixin, admin.TabularInline):
    model = OrderItems
    extra = 1


@admin.register(Order)
class OrdertAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('id', 'get_created_jalali', 'is_paid', 'discount', 'order_items_count_column', 'get_total_price')
    
    search_fields = ('id', 'create_datetime',)
    
    list_filter = ('create_datetime', 'is_paid')
    
    list_per_page = 10
    
    ordering = ('id', 'create_datetime',)
    
    # you can override formfield, for example:
    # formfield_overrides = {
    #     JSONField: {'widget': JSONEditor},
	# }
	

    inlines = [
        OrderItemsInline,
    ]

    
    def get_queryset(self, request):
        """
            Annotate with counts of related OrderItems instances.
        """
        
        queryset = super().get_queryset(request).annotate(
            order_items_count=Subquery(
                OrderItems.objects.filter(order_id=OuterRef('id')).values('order_id').annotate(
                    count=Count('order_id')).values('count'),
                output_field=models.IntegerField()
            ),
        )
        return queryset


    @admin.display(ordering="order_items_count", description=_("# items"))
    def order_items_count_column(self, order=Order):
        """
            We use this method to get the number of order`s items in the changelist.
        """
        url = (
            reverse("admin:order_orderitems_changelist")
            + "?"
            + urlencode({
                "order" : order.id,
            })
        )
        return format_html('<a href="{}" >{}</a>', url, order.order_items_count)
    
    
    @admin.display(ordering='create_datetime', description=_('create_datetime'))
    def get_created_jalali(self, obj):
        return datetime2jalali(obj.create_datetime).strftime('%A, %d %B %Y %H:%M:%S')



@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price', 'item_total_price')
    
    search_fields = ('product',)
    
    list_select_related = ('product', 'order')
    
    list_per_page = 10
    
    ordering = ('id',)
    
    def lookup_allowed(self, key, value):
        """
            We must override this method to use product as filter for show the product_images by using product_images_count_column method.
        """
        if key in ('order'):
            return True
        return super(ProductAdmin, self).lookup_allowed(key, value)

