from rest_framework import serializers

from . import models

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id', 'name']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = ['id', 'file', 'label']

class DishSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(read_only=True)
    # images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = models.Dish
        fields = ['id', 'name', 'category', 'description', 'price', 'restaurant', 'ratings', 'favourite', 'restaurant_details', 'images']

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Restaurant
        fields = [
            'id',
            'name',
            'description',
            'ratings',
        ]

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Driver
        fields = [
            'id',
            'user',
            'driver_id',
            'restaurant',
            'vehicle_color',
            'vehicle_description',
            'vehicle_number',
            'available',
            'current_location_latitude',
            'current_location_longitude',
        ]
    


class OrderItemSerializer(serializers.ModelSerializer):
    food_item = DishSerializer()

    class Meta:
        model = models.OrderItem
        fields = ['id', 'food_item', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = models.Order
        fields = ['id', 'user', 'total_price', 'created_at', 'is_delivered', 'assigned_driver', 'tracking_url', 'payment_status', 'items']



