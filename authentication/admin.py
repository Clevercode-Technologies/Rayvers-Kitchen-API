from django.contrib import admin
from .models import User, UserAddress, UserProfile
from rest_framework.authtoken.models import Token


# Register your models here.
admin.site.register(User)
admin.site.register(UserAddress)
admin.site.register(UserProfile)
# admin.site.unregister(Token)




