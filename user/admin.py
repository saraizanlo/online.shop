from django.contrib.admin import register, ModelAdmin
from user.models import Costumer

@register(Costumer)
class CostumerAdmin(ModelAdmin):
    list_display = [
        'name',
        'last_name',
        'username',
        'email'
    ]
    list_filter = [
        'name',
        'last_name',
        'username',
        'email'
    ]
    search_fields = [
        'name',
        'last_name',
        'username',
        'email'
    ]