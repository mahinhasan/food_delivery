from django.urls import path
from .views import (
    register, login, category_list_create, menu_item_list_create, create_order, 
    restaurant_list_create, restaurant_detail, category_detail, menu_item_detail, order_detail
)

app_name = 'restaurant'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('categories/', category_list_create, name='category-list-create'),
    path('categories/<int:pk>/', category_detail, name='category-detail'),
    path('menu-items/', menu_item_list_create, name='menu-item-list-create'),
    path('menu-items/<int:pk>/', menu_item_detail, name='menu-item-detail'),
    path('orders/', create_order, name='create-order'),
    path('orders/<int:pk>/', order_detail, name='order-detail'),
    path('restaurants/', restaurant_list_create, name='restaurant-list-create'),
    path('restaurants/<int:pk>/', restaurant_detail, name='restaurant-detail'),
]
