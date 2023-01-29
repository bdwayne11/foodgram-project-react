from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_staff
                or request.method in SAFE_METHODS)


class IsAuthorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                or request.method in SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
