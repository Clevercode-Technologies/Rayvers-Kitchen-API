# models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    ratings = models.IntegerField(default=0)
    # Other fields as needed will be here...

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Restaurants"
        verbose_name = "Restaurant"

class Dish(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="dish_category") 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    restaurant = models.ManyToManyField(Restaurant, related_name="restaurants", blank=True)
    ratings = models.IntegerField(default=0)
    favourite = models.ManyToManyField(User, related_name="favourites", blank=True)
    # Add other fields as needed...

    @property
    def get_category(self):
        return {
            "id": self.id,
            "name": self.category.name
        }

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Dishes"
        verbose_name = "Dish"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Dish, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)
    assigned_driver = models.ForeignKey('Driver', on_delete=models.CASCADE, null=True, blank=True)
    tracking_url = models.URLField(null=True, blank=True)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
    
    class Meta:
        verbose_name_plural = "Orders"
        verbose_name = "Order"

class OrderItem(models.Model):
    food_item = models.ForeignKey(Dish, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.food_item.name} in Order #{self.order.id}"
    
    class Meta:
        verbose_name_plural = "Order Items"
        verbose_name = "Order Item"

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    vehicle_number = models.CharField(max_length=20)
    available = models.BooleanField(default=True)
    current_location_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    current_location_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"Driver: {self.user.username}"
    
    class Meta:
        verbose_name_plural = "Drivers"
        verbose_name = "Driver"

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
    
    class Meta:
        verbose_name_plural = "Delivery Status"
        verbose_name = "Delivery Status"


class ShoppingCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Dish, through='CartItem')

    def __str__(self):
        return f"Shopping Cart for {self.user.username}"
    
    class Meta:
        verbose_name_plural = "Shopping Cart"
        verbose_name = "Cart"

class CartItem(models.Model):
    food_item = models.ForeignKey(Dish, on_delete=models.CASCADE)
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.food_item.name} in {self.cart}"
    
    class Meta:
        verbose_name_plural = "Cart Items"
        verbose_name = "Cart Item"

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id} via {self.payment_method} by {self.user.username}"

    class Meta:
        verbose_name_plural = "Payments"
        verbose_name = "Payment"
class PersonalMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"
    
    class Meta:
        verbose_name_plural = "Personal Messages"
        verbose_name = "Personal Message"





