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
        fields = ['id', 'name', 'category', 'description', 'price', 'restaurant', 'ratings', 'favourite']
    
    def get_category(self):
        return self.fields['category'].to_representation(self.instance.category)



    






