from django.contrib import admin
from django.contrib.admin import register, ModelAdmin
from product.models import Product, Comment, Rate, Category

@register(Product)
class ProductAdmin(ModelAdmin):
    list_display = [
        'name',
        'price',
        'category',
        'stock'
    ]

@register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = [
        'product',
        'comment_text',
        'costumer'
    ]

@register(Rate)
class RateAdmin(ModelAdmin):
    list_display = [
        'product',
        'costumer',
        'rate'
    ]

@register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = [
        'name',
    ]
