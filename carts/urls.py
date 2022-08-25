from django.urls import path
from .views import  cart_home, cart_update, quantity_update ,cart_checkout
urlpatterns = [
    path('', cart_home, name='home'),
    path('quantity-update/', quantity_update, name='quantity_update'),
    path('confirm/', cart_checkout, name='cart_checkout'),
    path('update/', cart_update, name='update'),
]

app_name = 'carts'