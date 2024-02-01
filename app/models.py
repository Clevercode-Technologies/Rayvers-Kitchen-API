# models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
# from .utils import generate_random_username
import random
import string

User = get_user_model()

def generate_random_username(length, max_attempts=100):
    for _ in range(max_attempts):
        random_username = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
        if not User.objects.filter(username=random_username).exists():
            return random_username
    raise ValueError('Could not generate a unique username after {} attempts'.format(max_attempts))

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    image = models.ImageField(verbose_name="category image", upload_to="category/", blank=False, null=False)
    
    def __str__(self):
        return self.name

class Restaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kitchen_id = models.CharField(_("Kitchen id"), max_length=20, blank=True, null=False)
    image = models.ImageField(verbose_name="restauarant image", upload_to="restaurant/", blank=False, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.TextField(blank=True)
    ratings = models.DecimalField(default=0, max_digits=3, decimal_places=1)
    # Other fields as needed will be here...

    def __str__(self):
        return f"Restaurant: {self.user.email}"
    
    class Meta:
        verbose_name_plural = "Restaurants"
        verbose_name = "Restaurant"

# Listens for chef that was created
@receiver(post_save, sender=User)
def create_restaurant(sender, instance=None, created=False, **kwargs):
    if created and instance.role == "chef":
        # Create a restaurant here
        restaurant = Restaurant.objects.create(user=instance)
        
        # Generate a unique username for the restaurant
        username = generate_random_username(8)
        while Restaurant.objects.filter(kitchen_id=username).exists():
            username = generate_random_username(8)
        # Set the username for the user and the restaurant
        instance.username = username
        instance.save()
        restaurant.kitchen_id = username
        restaurant.save()
        print("A restaurant was created")



class Image(models.Model):
    file = models.ImageField(verbose_name="dish image", upload_to="dishes/", blank=False, null=False)
    label = models.CharField(max_length=255, blank=True, null=False)

    def __str__(self):
        return self.file.url

class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)
    

    def __str__(self) -> str:
        return self.name
    

    
class Dish(models.Model):
    DELIVERY_OPTIONS = [
        ("free", "free"),
        ("paid", "paid")
    ]
    name = models.CharField(max_length=255, unique=True)
    images = models.ManyToManyField(Image, related_name='dish_images')
    description = models.TextField(blank=False, null=False)
    delivery_options = models.CharField(choices=DELIVERY_OPTIONS, max_length=5, default="free")
    time_duration = models.IntegerField(verbose_name="Time it takes to deliver.", help_text="In minutes.", default=0, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="dish_category") 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ingredients = models.ManyToManyField(Ingredient, related_name="dish_ingredients")
    restaurant = models.ForeignKey(Restaurant, related_name="restaurants", on_delete=models.CASCADE)
    ratings = models.DecimalField(default=0, max_digits=3, decimal_places=1)
    favourite = models.ManyToManyField(User, related_name="favourites", blank=True)

    # Add other fields as needed...

    @property
    def restaurant_details(self):
        restaurant = self.restaurant
        return {
            "name": restaurant.name,
            "ratings": restaurant.ratings,

        }

    @property
    def get_images(self):
        images = self.images.all()
        new_list = list(map(lambda x: {"label": x.label, "url":x.file.url}, images))
        return new_list
    

    @property
    def get_category(self):
        return {
            "id": self.id,
            "name": self.category.name,
            "image": self.category.image
        }

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Dishes"
        verbose_name = "Dish"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)
    assigned_driver = models.ForeignKey('Driver', on_delete=models.CASCADE, null=True, blank=True)
    tracking_url = models.URLField(null=True, blank=True)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} by {self.user.email}"
    
    class Meta:
        verbose_name_plural = "Orders"
        verbose_name = "Order"

class OrderItem(models.Model):
    food_item = models.ForeignKey(Dish, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.food_item.name} in Order #{self.order.id}"
    
    class Meta:
        verbose_name_plural = "Order Items"
        verbose_name = "Order Item"

class Driver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    driver_id = models.CharField(_("Driver id"), max_length=20, blank=True, null=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, blank=True, null=True)
    vehicle_color = models.CharField(max_length=40, blank=True, null=True)
    vehicle_description = models.TextField(blank=True, null=False)
    vehicle_number = models.CharField(max_length=40, blank=True, null=False)
    available = models.BooleanField(default=False)
    current_location_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    current_location_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"Driver: {self.user.email}"
    
    class Meta:
        verbose_name_plural = "Drivers"
        verbose_name = "Driver"

@receiver(post_save, sender=User)
def create_driver(sender, instance=None, created=False, **kwargs):
    if created and instance.role == "logistics":
        # Create a driver here
        driver = Driver.objects.create(user=instance)
        # Generate a unique username for the driver
        username = generate_random_username(8)
        while Driver.objects.filter(driver_id=username).exists():
            username = generate_random_username(8)
        # Set the username for the user and the driver
        instance.username = username
        instance.save()
        driver.driver_id = username
        driver.save()
        print("A driver was created")
        

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
        return f"Shopping Cart for {self.user.email}"
    
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
        return f"Payment for Order #{self.order.id} via {self.payment_method} by {self.user.email}"

    class Meta:
        verbose_name_plural = "Payments"
        verbose_name = "Payment"
class PersonalMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.email} to {self.receiver.email}"
    
    class Meta:
        verbose_name_plural = "Personal Messages"
        verbose_name = "Personal Message"





