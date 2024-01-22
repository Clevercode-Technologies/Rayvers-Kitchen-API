from rest_framework.permissions import BasePermission


class IsUserChef(BasePermission):
    """
    Allows access only to user who is a chef.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "chef")


class IsUserDriver(BasePermission):
    """
    Allows access only to user who is a driver.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "driver")
    

class IsUserCustomer(BasePermission):
    """
    Allows access only to user who is a driver.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "customer")












