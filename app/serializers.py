from rest_framework import serializers

from . import models

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id', 'name']


class DishSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(read_only=True)
    class Meta:
        model = models.Dish
        fields = ['id', 'name', 'get_images', 'category', 'description', 'price', 'restaurant', 'ratings', 'favourite', 'restaurant_details']
    
    def get_category(self):
        return self.fields['category'].to_representation(self.instance.category)

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
    







