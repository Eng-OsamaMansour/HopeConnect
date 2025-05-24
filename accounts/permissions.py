from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions
from accounts.models import Role

class RolePermission(BasePermission):
    allowed_roles: set[str] = set()

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in self.allowed_roles
        )

class IsAdmin(RolePermission):
    allowed_roles = Role.ADMIN

class IsDonor(RolePermission):
    allowed_roles = Role.DONOR

class IsOrphanage(RolePermission):
    allowed_roles = Role.ORPHANAGE

class IsVolunteer(RolePermission):
    allowed_roles = Role.VOLUNTEER

class IsLogistics(RolePermission):
    allowed_roles = Role.LOGISTICS

class OrphanageOrAdminPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if request.user.role == Role.ORPHANAGE:
            return obj.orphan.orphanage.manager == request.user
        return False
