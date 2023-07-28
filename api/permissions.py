from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

class DeyakkPermision(BasePermission):
    def has_permission(self, request, view):
        deyakk = User.objects.get(pk=3)
        return bool(request.method in SAFE_METHODS or request.user == deyakk and request or request.user.is_staff)
