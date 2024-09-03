from rest_framework.permissions import BasePermission

class IsOwnerOrEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['owner', 'employee']

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user in obj.employees.all()
