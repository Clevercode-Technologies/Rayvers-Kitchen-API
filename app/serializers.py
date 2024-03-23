from rest_framework import serializers

from . import models
from django.contrib.auth import get_user_model



User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id', 'name', 'image']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = ['id', 'file', 'label']

class DishSerializer(serializers.ModelSerializer):
    # Assuming you want to read the images
    images = ImageSerializer(many=True, read_only=True)  
    
    class Meta:
        model = models.Dish
        fields = [
            'id', 
            'name', 
            'delivery_options', 
            'time_duration', 
            'description', 
            'price', 
            'restaurant', 
            'ratings', 
            '_ingredients', 
            'favourite', 
            'restaurant_details', 
            'get_category', 
            'images', 
            'category',
            'image_url',
        ]

    def create(self, validated_data):

        # Create Dish instance
        
        ingredients = self.context['request'].data.get('ingredients', [])
        images_data = self.context['request'].data.get('images', [])

        

        # print("images_data: ", type(images_data))
        if not ingredients:
            # Check if the ingredients array have more than one ingredients id
            raise serializers.ValidationError(detail={"ingredients": ["ingredients is required"]})
        if not isinstance(ingredients, list) or not len(ingredients) > 0:
            # Perform a check to know if ingredients have been added to the database
            # Do this by checking there are ids in the array and finding out if these ids
            # belongs to a couple of ingredients

            raise serializers.ValidationError(detail={"ingredients": ["ingredients must be an array or list of ids"]})
            
        all_available_ingredients = models.Ingredient.objects.filter(id__in=ingredients)

        if not len(all_available_ingredients) > 0:
            raise serializers.ValidationError(detail={"ingredients": ["ingredients with ids do not exist."]})
    

        dish = super(DishSerializer, self).create(validated_data)


        # Add ingredient to dish
        try:
            for ing in all_available_ingredients:
                dish.ingredients.add(ing)
        except:
            pass

        try:
            images_data = self.context['request'].data.getlist('images', [])
            for image_file in images_data:
                image_instance = models.Image.objects.create(file=image_file)
                dish.images.add(image_instance)
        except:
            pass

        return dish


class DishSerializerForRating(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True) 
    class Meta:
        model = models.Dish
        fields = [
            'id', 
            'name',
            "images"
        ]

class DishRatingSerializer(serializers.ModelSerializer):
    dish = DishSerializerForRating(read_only=True)
    class Meta:
        model = models.DishRating
        fields = [
            "number",
            "text",
            "user_data",
            "dish",
        ]



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
            "_dishes",
            "image_url"
        ]


class RestaurantSerializerForRating(serializers.ModelSerializer):
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


class RestaurantRatingSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializerForRating(read_only=True)
    class Meta:
        model = models.RestaurantRating
        fields = [
            "number",
            "text",
            "user_data",
            "restaurant",
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
    
# A serializer for ordered dishes
class OrderedDishSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    class Meta:
        model = models.Dish
        fields = ['id', 'name', 'time_duration', 'description', 'price', 'restaurant', 'ratings','restaurant_details', 'get_category', 'images']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "is_staff",
            "is_active",
            "last_login",
            "is_superuser",
            "role",
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    dish = OrderedDishSerializer(read_only=True)
    driver = DriverSerializer(read_only=True)
    customer = UserSerializer(read_only=True)
    class Meta:
        model = models.OrderItem
        fields = ['id', 'quantity', 'amount', 'status', 'dish', 'driver', 'customer']



class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    

    class Meta:
        model = models.Order
        fields = [
            'id', 
            'user', 
            'total_price', 
            'created_at', 
            'is_delivered', 
            'payment_status', 
            'items'
        ]

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ingredient
        fields = "__all__"
