from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsStaffOrReadOnly(BasePermission):
    """
    Allows authenticated users to read, 
    but only Staff users to Create/Update/Delete.
    """
    def has_permission(self, request, view):
        # First, ensure the user is logged in (Satisfies Task 4.1)
        if not (request.user and request.user.is_authenticated):
            return False

        
        if request.method in SAFE_METHODS:
            return True

        
        return request.user.is_staff