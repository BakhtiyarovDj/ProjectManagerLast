from rest_framework import permissions

class IsProjectManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'project_manager'
    
class IsCaptain(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'captain'

