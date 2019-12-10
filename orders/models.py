from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=30, db_index=True)
    sized = models.BooleanField(default=True)
    slug = models.SlugField(max_length=200, unique=True)

    # Add class Meta to define plural form in model's name at the admin page
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("orders:menu_order", args=[self.slug])

class Size(models.Model):
    name = models.CharField(max_length=25, blank=True)

    def __str__(self):
        return f"{self.name}"

class Dish(models.Model):
    name = models.CharField(max_length=25)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="dishes")


    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Dishes"

class Product(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="dishes")
    size = models.ForeignKey(Size, default=None, on_delete=models.CASCADE, related_name="sizes")
    price = models.DecimalField(default=None, max_digits=10, decimal_places=2)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return f"{self.id}"

class Topping(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.name}"

# class Status(models.Model):
#     name = models.CharField(max_length=15, default="initiated")
#
#     def __str__(self):
#         return f"{self.name}"
#
#     class Meta:
#         verbose_name_plural = "Status"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    # total = models.DecimalField(max_digits=7, decimal_places=2)
    completed = models.BooleanField(default=False)
    # status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name="status")

    def __str__(self):
        return f"{self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    toppings = models.ManyToManyField(Topping, blank=True, default='')

    def __str__(self):
        return f"{self.id}"

    def get_cost(self):
        return self.price * self.quantity
