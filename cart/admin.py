from django.contrib.admin import register, ModelAdmin
from cart.models import Cart

@register(Cart)
class CartAdmin(ModelAdmin):
    list_display = [
        'code',
        'costumer',
        'is_finalized'
    ]