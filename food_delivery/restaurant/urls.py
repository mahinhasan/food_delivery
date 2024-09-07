from django.urls import path
from .views import register, login, category_list_create, menu_item_list_create, create_order,restaurant_list_create,restaurant_detail

app_name = 'restaurant'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('categories/', category_list_create, name='category-list-create'),
    path('menu-items/', menu_item_list_create, name='menu-item-list-create'),
    path('orders/', create_order, name='create-order'),
    path('restaurants/', restaurant_list_create, name='restaurant-list-create'),
    path('restaurants/<int:pk>/', restaurant_detail, name='restaurant-detail'),
]
