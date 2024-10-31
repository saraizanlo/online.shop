from django.contrib import admin
from django.contrib.admin import register, ModelAdmin
from order.models import Order, Discount

@register(Order)
class OrderAdmin(ModelAdmin):
    list_display = [
        'code',
        'costumer',
        'discount',
        'cart',
        'is_received',
    ]

@register(Discount)
class DiscountAdmin(ModelAdmin):
    list_display = [
        'code',
        'percentage',
       'start_date',
        'end_date',
    ]
