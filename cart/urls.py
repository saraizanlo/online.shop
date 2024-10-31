from django.urls import path
from cart.views import add_product_to_cart, remove_product_from_cart, finalize_cart, view_active_cart

urlpatterns = [
    path('add_product_to_cart/', add_product_to_cart),
    path('remove_product_from_cart/', remove_product_from_cart),
    path('finalize_cart/', finalize_cart),
    path('view_active_cart/', view_active_cart)
]