from functools import reduce
import stripe

from decouple import config
# views.py
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem, Dish, Restaurant, Driver
from .serializers import OrderSerializer, OrderItemSerializer, DishSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from app.permissions import IsUserVerified
from rest_framework.views import APIView


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    # authentication_classes = []
    # permission_classes = []
    # pagination_class = []

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    # authentication_classes = []
    # permission_classes = []
    # pagination_class = []

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user).order_by('-created_at')
    


    # def retrieve(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())  # Get all instances
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data) 

    def create(self, request, *args, **kwargs):
        
        data = request.data
        items_data = data.pop('items')
        if len(items_data) < 1:
            return Response({"message": "There must be ordered items in the payload"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not isinstance(items_data, list):
            return Response({"message": "Invalid data structure for items. Items must be an array of ordered items."}, status=status.HTTP_400_BAD_REQUEST)
        
        total_price = reduce(lambda x, y: x + (float(y.get("amount", 0)) * int(y.get("quantity", 0))), items_data, 0)

        # print("Total price", total_price == data.get("total_price"))

        if float(total_price) != float(data.get("total_price")):
            return Response({"message": "Conflict in total price. There is a difference between the total price of items and that of the general total price."})
        # Assuming the request data has 'user', 'items', and other necessary fields
        # serializer = self.get_serializer(data=data)
        # items = data.get("items")
        data.pop("user")
        order = Order.objects.create(user=request.user, **data)
        for item in items_data:
            dish_id = item.get("dish_id")
            restaurant_id = item.get("restaurant_id")
            try:
                dish = Dish.objects.get(id=item.pop('dish_id'))
            except Dish.DoesNotExist:
                return Response({"message": f"Dish with id: {dish_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)
            try:
                restaurant = Restaurant.objects.get(id=item.pop("restaurant_id"))
            except Restaurant.DoesNotExist:
                return Response({"message": f"Restaurant with id: {restaurant_id} does not exists"}, status=status.HTTP_400_BAD_REQUEST)
            
            OrderItem.objects.create(order=order, dish=dish, restaurant=restaurant, **item)

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class OrderCustomerListView(APIView):
    serializer_class = OrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        if not data.get("items"):
            return Response({"message": "No items or colletion of items in the payload -- items field is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        items_data = data.pop('items')
        if len(items_data) < 1:
            return Response({"message": "There must be ordered items in the payload"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not isinstance(items_data, list):
            return Response({"message": "Invalid data structure for items. Items must be an array of ordered items."}, status=status.HTTP_400_BAD_REQUEST)
        
        total_price = reduce(lambda x, y: x + (float(y.get("amount", 0)) * int(y.get("quantity", 0))), items_data, 0)

        # print("Total price", total_price == data.get("total_price"))

        if int(total_price) != int(data.get("total_price")):
            return Response({"message": "Conflict in total price. There is a difference between the total price of items and that of the general total price."})
        # Assuming the request data has 'user', 'items', and other necessary fields
        # serializer = self.get_serializer(data=data)
        # items = data.get("items")
        # if data.get("user"):
        #     data.pop("user")
        order = Order.objects.create(user=request.user, **data)
        for item in items_data:
            dish_id = item.get("dish_id")
            restaurant_id = item.get("restaurant_id")
            amount = item.get("amount")
            quantity = item.get("quantity")


            try:
                dish = Dish.objects.get(id=item.pop('dish_id'))
            except Dish.DoesNotExist:
                return Response({"message": f"Dish with id: {dish_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)
            try:
                restaurant = Restaurant.objects.get(id=item.pop("restaurant_id"))
            except Restaurant.DoesNotExist:
                return Response({"message": f"Restaurant with id: {restaurant_id} does not exists"}, status=status.HTTP_404_NOT_FOUND)
            
            if int(amount) != int(dish.price):
                return Response({"message": f"The amount {int(amount)} entered for dish with id {dish.id} does not correlate with the price of dish {dish.price}"}, status=status.HTTP_400_BAD_REQUEST)
            
            OrderItem.objects.create(order=order, dish=dish, restaurant=restaurant, **item)

        serializer = self.serializer_class(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    

class OrderItemsListForAllUsers(APIView):
    serializer_class = OrderItemSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Check the user that is requesting for the ordered items
        # If the user is a customer, fetch all Customer his order
        # If the user is a restaurant, get all the orders for that restaurant
        # If the user is a driver, get all the orders for the assigned driver

        query_params = request.query_params

        # Check the query parameters to the option key
        # If the option is history, let all the orderitems completed and cancelled be shown
        # If the option is ongoing, let all the orderitems pending be shown
        # Else if option is not specified, let all the orderitems be shown
        option = query_params.get("option")
        ordereditems = OrderItem.objects.all()
        if option == "history":
            ordereditems = ordereditems.exclude(status="pending")
        elif option == "ongoing":
            ordereditems = ordereditems.filter(status="pending").exclude(status="completed").exclude(status="cancelled")
        else:
            pass

        user = request.user

        user_is_customer = user.role == "customer"
        user_is_driver = user.role == "logistics"
        user_is_restaurant = user.role == "chef"

        # print("user_is_customer: ", user_is_customer)
        # print("user_is_driver: ", user_is_driver)
        # print("user_is_restaurant: ", user_is_restaurant)

        if user_is_customer:
            # User is a customer
            ordereditems = ordereditems.filter(order__user_id=request.user.id)
            serializer = self.serializer_class(ordereditems, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif user_is_restaurant:
            ordereditems = ordereditems.filter(restaurant__user_id=user.id)
            # User is a Restaurant or Kitchen
            serializer = self.serializer_class(ordereditems, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif user_is_driver:
            # User is a driver
            ordereditems = ordereditems.filter(driver__user_id=user.id)
            serializer = self.serializer_class(ordereditems, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "User must be one of the following: restaurant, driver or customer"}, status=status.HTTP_400_BAD_REQUEST)
    
    
class OrderItemsDetailsForAllUsers(APIView):
    serializer_class = OrderItemSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        try:
            orderitem = OrderItem.objects.get(pk=pk)
        except OrderItem.DoesNotExist:
            return Response({"message": f"Order item with id: {pk} does not exist"})
        
        user = request.user

        user_is_customer = user.role == "customer"
        user_is_driver = user.role == "logistics"
        user_is_restaurant = user.role == "chef"

        serializer = self.serializer_class(orderitem)

        # Check the user permission if the user is either of the following:
        # customer, chef and driver

        if user_is_customer:
            # Check if user is customer and it is them who made the order
            if orderitem.order.user.id != user.id:
                return Response({"message": "User does not have permission to view this order item"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(serializer.data, status=status.HTTP_200_OK)
        elif user_is_restaurant:
            # Check if user is restaurant and it is them who are receiving the order
            if orderitem.restaurant.user.id != user.id:
                return Response({"message": "User does not have permission to view this order item"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(serializer.data, status=status.HTTP_200_OK)
        elif user_is_driver:
            # Check if user is driver and it is them who are delivering or being assigned to the order
            if not orderitem.driver:
                return Response({"message": "User does not have permission to view this order item"}, status=status.HTTP_401_UNAUTHORIZED)
            if orderitem.driver.user.id != user.id:
                return Response({"message": "User does not have permission to view this order item"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "User must be one of the following: restaurant, driver or customer"}, status=status.HTTP_400_BAD_REQUEST)

    
    def put(self, request, *args, **kwargs):
        # Get the driver or status --- completed, pending, cancelled

        pk = kwargs["pk"]
        
        data = request.data
        # The current user can send the driver_id or the status, at anytime they wishes
        

        # Get the orderitem
        try:
            orderitem = OrderItem.objects.get(pk=pk)
        except OrderItem.DoesNotExist:
            return Response({"message": "Ordered item does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        # Get OrderItemSerializer
        serializer = self.serializer_class(orderitem, data=request.data)
        # If there is no error, save it
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Order item updated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_201_CREATED)
    
    

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsUserVerified])
def payment_intent_stripe(request):
    stripe.api_key = config("STRIPE_SECRET_KEY")

    amount = int(float(request.data.get("amount")))
    currency_code = request.data.get("currency_code")

    try:
        payment_intent_stripe = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency_code,
            automatic_payment_methods={"enabled": True},
        )
        return Response({"payment_intent_secret": payment_intent_stripe.client_secret}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": f"Something went wrong: {e}"}, status=status.HTTP_400_BAD_REQUEST)


