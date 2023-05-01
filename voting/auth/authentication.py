from rest_framework.permissions import BasePermission

class IsAuthenticated(BasePermission):
    def authenticate(self, request):
        return request.user and request.user.is_authenticated