from django.contrib import admin
from .models import (
    Restaurant,
    Category,
    Dish,
    OrderItem,
    Order,
    Driver,
    DeliveryStatus,
    ShoppingCart,
    CartItem,
    Payment,
    PersonalMessage,
)

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(Category)
admin.site.register(Dish)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Driver)
admin.site.register(DeliveryStatus)
admin.site.register(ShoppingCart)
admin.site.register(CartItem)
admin.site.register(Payment)
admin.site.register(PersonalMessage)

