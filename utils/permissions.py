from rest_framework.views import Request, View
from rest_framework import permissions
from products.models import Product


class IsSellerOrReadOnly(permissions.BasePermission):
    def has_permission(self, req: Request, view: View):
        return bool(
            req.method in permissions.SAFE_METHODS
            or req.user.is_authenticated
            and req.user.is_seller
        )


class IsSellerAndOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, req: Request, view: View, obj: Product):
        return bool(
            req.method in permissions.SAFE_METHODS
            or req.user.is_authenticated
            and req.user.is_seller
            and obj.user == req.user
        )


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, req: Request, view: View, obj: Product):
        return bool(req.user.is_authenticated and obj == req.user)


class IsAdmin(permissions.BasePermission):
    def has_permission(self, req: Request, view: View):
        return bool(req.user.is_authenticated and req.user.is_superuser)
