from django.urls import path, include
# from rest_framework.authtoken import views
from . import views

app_name = "authentication"

urlpatterns = [
    path("token/", views.CustomAuthToken.as_view(), name="token"),
    path("logout/", views.logoutView, name="logout"),
    path("users/", views.create_new_user, name="create_user"),
    path("users/me/", views.get_current_user_profile, name="profile"),
]




