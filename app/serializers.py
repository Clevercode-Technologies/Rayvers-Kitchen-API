from rest_framework import serializers

from . import models

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id', 'name', 'image']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = ['id', 'file', 'label']

class DishSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(read_only=True)
    images = ImageSerializer(many=True, read_only=True)  # Assuming you want to read the images
    
    class Meta:
        model = models.Dish
        fields = ['id', 'name', 'description', 'price', 'restaurant', 'ratings', '_ingredients', 'favourite', 'restaurant_details', 'get_category', 'images', 'category']

    def create(self, validated_data):
        images_data = self.context['request'].data.getlist('images', [])

        print("images_data: ", type(images_data))

        # Create Dish instance
        dish = super(DishSerializer, self).create(validated_data)
        for image_file in images_data:
            image_instance = models.Image.objects.create(file=image_file)
            dish.images.add(image_instance)

        return dish

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Restaurant
        fields = [
            'id',
            'name',
            'description',
            'ratings',
            'image',
            'address',
        ]

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Driver
        fields = [
            'id',
            'driver_id',
            'vehicle_image',
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



