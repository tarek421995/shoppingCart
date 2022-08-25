from atexit import register
from django.contrib import admin

from .models import Cart, CartItem, Item

# Register your models here.

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Item)