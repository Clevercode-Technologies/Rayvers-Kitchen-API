from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from app.permissions import IsRestaurantUser
from app.models import Driver, Restaurant

from . import serializers
from .helpers import check_email, is_valid_password


User = get_user_model()

from .helpers import (
    check_email, 
    is_valid_password, 
    generate_4_digit_code, 
    send_registration_code_mail, 
    check_if_code_matches,
)


# RESTAURANT AUTH VIEWS
@api_view(['POST'])
def login_restaurant(request):
    data = request.data
    kitchen_id = data.get("kitchen_id")
    password = data.get("password")

    if not kitchen_id:
        return Response({"detail": "kitchen_id is required"}, status=status.HTTP_400_BAD_REQUEST)
    if not password:
        return Response({"detail": "password is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Search if the restaurant exists in either the Restaurant or User models
    try:
        user = User.objects.filter(username=kitchen_id).first()
    except User.DoesNotExist:
        user = None
        return Response({"detail": "user does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    
    try:
        restaurant = Restaurant.objects.filter(kitchen_id=kitchen_id).first()
    except Restaurant.DoesNotExist:
        restaurant = None
        return Response({"detail": "kitchen does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    
    if not user.is_verified:
        return Response({"message": "User is not verified"}, status=status.HTTP_401_UNAUTHORIZED)
    
    if user and restaurant:
        # If both a user and a restaurant were found for that username/kitchen_id, check passwords
        if user.check_password(password):
            return Response({
                "token": user.auth_token.key, 
                "user_id": user.id, 
                "kitchen_id": user.username, 
                # "email": user.email
            }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "user with kitchen id does exists"}, status=status.HTTP_400_BAD_REQUEST)



# This api view should only be assessed by admins | only admins can create kitchen
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def create_restaurant(request):
    """
    Creates Restaurant
    @payload: email, password
    """
    data = request.data
    email = data.get("email")
    password = data.get("password")

    # Create restaurant user
    # Check if user already exists
    # If user exists, do not create user
    if not email:
        return Response({
            "email": [
                "This field may not be blank."
            ]
        }, status=status.HTTP_400_BAD_REQUEST)
    elif not password:
        return Response({
            "password": [
                "This field may not be blank."
            ]
        }, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Check if email and password are valid entry
        email_valid_status = check_email(email)
        password_valid_status = is_valid_password(password)
        if email_valid_status.status == False:
            return Response({
                "email": [
                    error_message for error_message in email_valid_status.error_messages
                ]
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if password_valid_status.status == False:
            return Response({
                "password": [
                    error_message for error_message in password_valid_status.error_messages
                ]
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user already exists
        existing_user = User.objects.filter(email=email)
        if len(existing_user) > 1 or existing_user:
            return Response({
                "email": [
                    "User with email already exists."
                ]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Finally create user Create user
            code = generate_4_digit_code()
            data.update({"role": "chef", "code": code})

            serializer = serializers.UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                # Object / Dictionary to be returned after user has been created
                user_details = {
                    "message": f"A verification code has been sent to {serializer.data.get('email')}.",
                    "user_id": serializer.data.get("id"),
                    "kitchen_id": serializer.data.get("username"),
                    "role": serializer.data.get("role"),
                }
                response_gotten_from_code = send_registration_code_mail(code, serializer.data.get('email'))
                print("The response status I got from the code registration: ", response_gotten_from_code)

                return Response(user_details, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# DRIVER AUTH VIEWS
@api_view(['POST'])
def login_driver(request):
    data = request.data
    driver_id = data.get("driver_id")
    password = data.get("password")

    if not driver_id:
        return Response({"detail": "driver_id is required"}, status=status.HTTP_400_BAD_REQUEST)
    if not password:
        return Response({"detail": "password is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Search if the driver exists in either the Driver or User models
    try:
        user = User.objects.filter(username=driver_id).first()
    except User.DoesNotExist:
        user = None
        return Response({"detail": "user does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        driver = Driver.objects.filter(driver_id=driver_id).first()
    except Driver.DoesNotExist:
        driver = None
        return Response({"detail": "driver does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    
    if not user.is_verified:
        return Response({"message": "User is not verified"}, status=status.HTTP_401_UNAUTHORIZED)
    
    if user and driver:
        # If both a user and a driver were found for that username/ID, check passwords
        if user.check_password(password):
            return Response({
                "token": user.auth_token.key, 
                "user_id": user.id, 
                "driver_id": user.username, 
                "email": user.email
            }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "user with driver id does exists"}, status=status.HTTP_400_BAD_REQUEST)


# This api view should only be assessed by restaurants (kitchens) and admin
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated & (IsAdminUser | IsRestaurantUser)])
def create_driver(request):
    data = request.data
    email = data.get("email")
    password = data.get("password")

    # Create driver user
    # Check if user already exists
    # If user exists, do not create user
    if not email:
        return Response({
            "email": [
                "This field may not be blank."
            ]
        }, status=status.HTTP_400_BAD_REQUEST)
    elif not password:
        return Response({
            "password": [
                "This field may not be blank."
            ]
        }, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Check if email and password are valid entry
        email_valid_status = check_email(email)
        password_valid_status = is_valid_password(password)
        if email_valid_status.status == False:
            return Response({
                "email": [
                    error_message for error_message in email_valid_status.error_messages
                ]
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if password_valid_status.status == False:
            return Response({
                "password": [
                    error_message for error_message in password_valid_status.error_messages
                ]
            }, status=status.HTTP_400_BAD_REQUEST)

        # Lastly Check if user already exists
        existing_user = User.objects.filter(email=email)
        if len(existing_user) > 1 or existing_user:
            return Response({
                "email": [
                    "User with email already exists."
                ]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Finally create user Create user
            if request.user.role != "chef":
                return Response({
                    "detail": "only restaurants and admins have permission to add drivers"
                }, status=status.HTTP_400_BAD_REQUEST)

            data.update({"role": "logistics"})
            serializer = serializers.UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                if request.user.role == "chef":
                    # Query for the user restaurant model if user is chef
                    restaurant = Restaurant.objects.filter(user=request.user).first()
                    # Get the Driver
                    driver = Driver.objects.filter(driver_id=serializer.data.get("username")).first()
                    # Assign the driver to the restaurant
                    driver.restaurant = restaurant
                    driver.save()
                # Object / Dictionary to be returned after user has been created
                user_details = {
                    "user_id": serializer.data.get("id"),
                    "username": serializer.data.get("username"),
                    "email": serializer.data.get("email"),
                    "is_staff": serializer.data.get("is_staff"),
                    "last_login": serializer.data.get("last_login"),
                    "user_permissions": serializer.data.get("user_permissions"),
                    "is_superuser": serializer.data.get("is_superuser"),
                    "role": serializer.data.get("role"),
                    "token":  User.objects.get(id=serializer.data.get("id")).auth_token.key,
                    "password": User.objects.get(id=serializer.data.get("id")).password
                }
                return Response(user_details, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
