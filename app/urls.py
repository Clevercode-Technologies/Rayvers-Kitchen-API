from django.urls import path 
from . import views


urlpatterns = [

    path('', views.HomeAPIViewList.as_view(), name="general_api_view"),


    path('categories/', views.CategoryViewList.as_view(), name="category_list"),
    path('categories/<int:pk>/', views.CategoryViewDetails.as_view(), name="category_detail"),

    path('dishes/', views.DishesViewList.as_view(), name="dish_list"),
    path('dishes/<int:pk>/', views.DishesViewDetails.as_view(), name="dish_detail"),

    path("restaurants/", views.ResturantViewList.as_view(), name="restaurant_list"),
    path("restaurants/<int:pk>/", views.RestaurantViewDetails.as_view(), name="restaurant_detail"),

    path("drivers/", views.DriversViewList.as_view(), name="driver_list"),
    path("drivers/<int:pk>/", views.DriverViewDetails.as_view(), name="driver_detail"),
    
] 





