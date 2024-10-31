from django.urls import path
from order.views import finalize_order, view_costumer_orders

urlpatterns = [
    path('finalize_order/<str:order_id>/', finalize_order),
    path('view_costumer_orders/', view_costumer_orders)
]