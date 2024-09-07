from django.contrib.auth.models import AbstractUser
from django.db import models



# abstruct user is built in user modify to add extra field for authentication
class User(AbstractUser):
    is_owner = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.SET_NULL, null=True, blank=True)
  

# name of the restaurant
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name='owned_restaurants', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# category model - food category
class Category(models.Model):
    name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant, related_name='categories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# menu items of food
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='menu_items', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Modifier(models.Model):
    name = models.CharField(max_length=100)
    menu_item = models.ForeignKey(MenuItem, related_name='modifiers', on_delete=models.CASCADE)
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, related_name='orders', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=[('cash', 'Cash'), ('card', 'Card')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.customer.username}"
