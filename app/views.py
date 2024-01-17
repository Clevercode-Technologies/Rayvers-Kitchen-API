from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from . import serializers
from .import models

# Create your views here.

# Custom Paginator class
class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# ------------------------------- Home views -----------------------------------
class HomeAPIViewList(APIView):
    def get(self, request):
        return Response({"message": "Welcome to Reyvers Kitchen API"})
    

# ------------------------------- Category views -----------------------------------
class CategoryViewList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class =  serializers.CategorySerializer
    pagination_class = CustomPageNumberPagination
    

    def get(self, *args, **kwargs):
        """Returns a list of all categories"""
        categories = models.Category.objects.all()
        paginator = CustomPageNumberPagination()

        # Use the pagination class to paginate the queryset
        paginated_categories = paginator.paginate_queryset(categories, self.request)

        serializer = self.serializer_class(paginated_categories, many=True)
        
        return Response({
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'results': serializer.data
        })
        

    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CategoryViewDetails(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class =  serializers.CategorySerializer

    def get(self, *args, **kwargs):
        """Returns a category detail and paginated dishes under the category"""
        pk = kwargs["pk"]
        category = get_object_or_404(models.Category, pk=pk)
        serializer = self.serializer_class(category)

        # Get all the dishes under this category
        dishes = models.Dish.objects.filter(category__id=pk)

        # Use the pagination class to paginate the dishes queryset
        paginator = CustomPageNumberPagination()
        paginated_dishes = paginator.paginate_queryset(dishes, self.request)

        # Serialize the paginated dishes
        dishes_serialized = serializers.DishSerializer(paginated_dishes, many=True)

        context = {
            "category": {
                "id": serializer.data.get("id"),
                "name": serializer.data.get("name"),
                "dishes": {
                    "count": paginator.page.paginator.count,
                    "next": paginator.get_next_link(),
                    "previous": paginator.get_previous_link(),
                    "results": dishes_serialized.data
                }
            }
        }

        return Response(context, status=status.HTTP_200_OK)

    def put(self, *args, **kwargs):
        pk = kwargs["pk"]
        category = get_object_or_404(models.Category, pk=pk)
        serializer = self.serializer_class(instance=category, data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, *args, **kwargs ):
        pk = kwargs["pk"]
        try:
            category = models.Category.objects.get(pk=pk)
            category.delete()
            return Response({"details": "category has been deleted successfully "}, status=status.HTTP_204_NO_CONTENT)
        except models.Category.DoesNotExist:
            return Response({"details": "category with id not found"}, status=status.HTTP_404_NOT_FOUND)




# ------------------------------- Dish views -----------------------------------
class DishesViewList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.DishSerializer

    pagination_class = CustomPageNumberPagination

    def get(self, *args, **kwargs ):
        """Returns a list of all dishes"""
        dishes = models.Dish.objects.all()

        paginator = CustomPageNumberPagination()

        paginated_dishes = paginator.paginate_queryset(dishes, self.request)

        serializer = self.serializer_class(paginated_dishes, many=True)
    
        return Response({
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'results': serializer.data
        })

    def post(self, *args, **kwargs ):
        data = self.request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class DishesViewDetails(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        pk = kwargs["pk"]
        try:
            dish = models.Dish.objects.get(pk=pk)
            serializer = serializers.DishSerializer(dish)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.Dish.DoesNotExist:
            return Response({"details": "dish with id not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, *args, **kwargs):
        pk = kwargs["pk"]
        dish = get_object_or_404(models.Dish, pk=pk)
        serializer = self.serializer_class(instance=dish, data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, *args, **kwargs):
        pk = kwargs["pk"]
        try:
            dish = models.Dish.objects.get(pk=pk)
            dish.delete()
            return Response({"details": "dish has been deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except models.Dish.DoesNotExist:
            return Response({"details": "dish with id not found"}, status=status.HTTP_404_NOT_FOUND)
        
    

# ------------------------------- Restaurant views -----------------------------------
class ResturantViewList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response({"message": "Hello"})

    def post(self, request):
        return Response({"message": "Hello"})
    
class RestaurantViewDetails(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        return Response({"message": "Hello"})

    def put(self, request, pk):
        return Response({"message": "Hello"})
    
    def delete(self, request, pk):
        return Response({"message": "Hello"})
    

# ------------------------------- Driver views -----------------------------------
class DriversViewList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Hello"})

    def post(self, request):
        return Response({"message": "Hello"})
    
class DriverViewDetails(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        return Response({"message": "Hello"})

    def put(self, request, pk):
        return Response({"message": "Hello"})
    
    def delete(self, request, pk):
        return Response({"message": "Hello"})
    

# ------------------------------- Order views -----------------------------------

class OrderViewList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # pagination_classes = 

    def get(self, request):
        # Get the user
        # Get all the recent order of the user
        return Response({"message": "Hello"})

    def post(self, request):
        return Response({"message": "Hello"})
    


class OrderViewDetails(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        return Response({"message": "Hello"})

    def put(self, request, pk):
        return Response({"message": "Hello"})
    
    def delete(self, request, pk):
        return Response({"message": "Hello"})




