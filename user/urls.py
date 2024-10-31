from django.urls import path
from user.views import costumers, add_costumer, add_money_to_wallet, reset_password, update_costumer, get_costumer

urlpatterns = [
    path('costumers', costumers),
    path('add_costumer', add_costumer),
    path('add_money_to_wallet', add_money_to_wallet),
    path('reset_password', reset_password),
    path('update_costumer', update_costumer),
    path('get_costumer/<str:costumer_id>', get_costumer)

]