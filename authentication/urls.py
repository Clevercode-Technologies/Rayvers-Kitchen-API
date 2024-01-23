from django.urls import path, include
# from rest_framework.authtoken import primary_views
from . import views as primary_views
from . import action_views as secondary_views

app_name = "authentication"

urlpatterns = [
    # Primary Views
    path('', primary_views.HomeAPIAuthViewList.as_view(), name="general_api_view"),
    path("token/", primary_views.CustomAuthToken.as_view(), name="token"),
    path("logout/", primary_views.logoutView, name="logout"),
    path("users/", primary_views.create_new_user, name="create_user"),
    path("users/me/", primary_views.get_current_user_profile, name="profile"),
    path("users/addresses/", primary_views.current_user_address_view, name="address_list"),
    path("users/addresses/<int:pk>/", primary_views.detail_user_address_view, name="address_detail"),

    # Secondary Views
    path("drivers/token/", secondary_views.login_driver, name="login_driver"),
    path("drivers/", secondary_views.create_driver, name="create_driver"),
]




