from django.urls import path
from product.views import products, products_comments, rate_product, add_comment, add_product, get_product, add_rate

urlpatterns = [
    path('products', products),
    path('products/<int:product_id>/comments', products_comments),
    path('products/<int:product_id>/rate', rate_product),
    path('add_comment', add_comment),
    path('add_product', add_product),
    path('get_product/<int:product_id>', get_product),
    path('add_rate', add_rate),
]