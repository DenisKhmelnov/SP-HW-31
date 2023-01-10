from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    message = "You have no access for this selection"

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        else:
            return False