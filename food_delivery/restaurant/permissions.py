from rest_framework.permissions import BasePermission

class IsOwnerOrEmployee(BasePermission):
    """
    Custom permission to only allow owners or employees of a restaurant to access the view.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (getattr(request.user, 'is_owner', False) or getattr(request.user, 'is_employee', False))
        )

class IsRestaurantUser(BasePermission):
    """
    Custom permission to only allow users associated with a specific restaurant.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'restaurant') and
            request.user.restaurant is not None
        )
