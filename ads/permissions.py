from rest_framework.permissions import BasePermission

from users.models import UserRoles


class IsOwner(BasePermission):
    message = "You have no access for this selection"

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        else:
            return False


class IsOwnerOrStaff(BasePermission):
    message = "You have no access for this Ad"

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author or request.user.role in [UserRoles.ADMIN, UserRoles.MODERATOR]:
            return True
        else:
            return False