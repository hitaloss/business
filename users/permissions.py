from rest_framework import permissions


class UserIsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        return request.user.id == obj.id


class UserIsAdm(permissions.BasePermission):
    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        return request.user.is_superuser
