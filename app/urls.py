from django.urls import path, include
from . import views as primary_views
from . import action_views as secondary_views

from rest_framework.routers import DefaultRouter

from .action_views import OrderViewSet, OrderItemViewSet, DishViewSet


router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'orderitems', OrderItemViewSet)
router.register(r'dishes', DishViewSet)


urlpatterns = [
    # Primary Views
    path('', primary_views.HomeAPIViewList.as_view(), name="general_api_view"),


    path('categories/', primary_views.CategoryViewList.as_view(), name="category_list"),
    path('categories/<int:pk>/', primary_views.CategoryViewDetails.as_view(), name="category_detail"),

    path('dishes/', primary_views.DishesViewList.as_view(), name="dish_list"),
    path('dishes/<int:pk>/', primary_views.DishesViewDetails.as_view(), name="dish_detail"),

    path("restaurants/", primary_views.ResturantViewList.as_view(), name="restaurant_list"),
    path("restaurants/<int:pk>/", primary_views.RestaurantViewDetails.as_view(), name="restaurant_detail"),

    path("drivers/", primary_views.DriversViewList.as_view(), name="driver_list"),
    path("drivers/<int:pk>/", primary_views.DriverViewDetails.as_view(), name="driver_detail"),

    # Secondary Views
    path('custom/', include(router.urls)),
    
    
] 





