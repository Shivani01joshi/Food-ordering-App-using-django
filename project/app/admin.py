from django.contrib import admin

from .models import Cart, CartItems, Pizza, PizzaCategory

# Register your models here.
admin.site.register(PizzaCategory)
admin.site.register(Pizza)
admin.site.register(Cart)
admin.site.register(CartItems)
