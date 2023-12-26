# в файле urls.py вашего приложения

from django.urls import path
from .views import orders_list, order_detail, create_order, process_order, login, profile, logout, index, register

urlpatterns = [
    path('', index, name='index'),
    path('orders/', orders_list, name='orders_list'),
    path('orders/<int:order_id>/', order_detail, name='order_detail'),
    path('orders/create/', create_order, name='create_order'),
    path('orders/process/<int:order_id>/', process_order, name='process_order'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
]
