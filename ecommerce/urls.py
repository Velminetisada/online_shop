from django.contrib import admin
from django.urls import path
from shop_products.views import (
    home,
    add_to_cart,
    cart,
    remove_from_cart,
    increase_quantity,
    decrease_quantity,
    checkout,
    register,
    user_login,
    user_logout,
    order_history,
    payment,
)
urlpatterns = [
    path('payment/', payment, name='payment'),
    path('orders/', order_history, name='order_history'),
    path('admin/', admin.site.urls),

    path('', home, name='home'),

    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),

    path('cart/', cart, name='cart'),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('increase/<int:product_id>/', increase_quantity, name='increase_quantity'),
    path('decrease/<int:product_id>/', decrease_quantity, name='decrease_quantity'),

    path('checkout/', checkout, name='checkout'),

    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]