from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='restaurant_logos/', null=True, blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class FoodItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='food_item_images/', null=True, blank=True)

    def __str__(self):
        return self.name
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(FoodItem, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)
    assigned_driver = models.ForeignKey('Driver', on_delete=models.SET_NULL, null=True, blank=True)
    tracking_url = models.URLField(null=True, blank=True)  # URL for real-time tracking

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.food_item.name} in Order #{self.order.id}"

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vehicle_number = models.CharField(max_length=20)
    available = models.BooleanField(default=True)
    current_location_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    current_location_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"Driver: {self.user.username}"

class DeliveryStatus(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    status_choices = [
        ('PENDING', 'Pending'),
        ('OUT_FOR_DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='PENDING')

    def __str__(self):
        return f"Status for Order #{self.order.id}: {self.status}"