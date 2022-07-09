from django.contrib.auth.models import User
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.dono == request.user


class IsUpdateProfile(permissions.BasePermission):

      def has_permission(self, request, view):
           if request.method in permissions.SAFE_METHODS: ## if have more condition then apply
              return True
           return request.user == User.objects.get(pk=view.kwargs['id'])