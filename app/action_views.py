# views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem, Dish
from .serializers import OrderSerializer, OrderItemSerializer, DishSerializer

class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    # authentication_classes = []
    # permission_classes = []
    # pagination_class = []

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        # Assuming the request data has 'user', 'items', and other necessary fields
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
