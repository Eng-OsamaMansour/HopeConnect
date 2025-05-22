from rest_framework import  viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.models import Role
from .serializers import RegisterSerializer, UserMeSerializer
from .permissions import IsAdmin         
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginView(TokenObtainPairView):
    """POST /auth/login/  (anonymous → tokens)"""
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response

class LogoutView(viewsets.ViewSet):
    """POST /auth/logout/  (authenticated → blacklist token)"""
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def logout(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    """
    GET     /users/                  (admin → list users)
    POST    /users/                  (anonymous → create user with limited roles, admin → create any role) 
    GET     /users/{id}/             (admin/self → user details)
    PATCH   /users/{id}/            (admin/self → update user)
    DELETE  /users/{id}/            (self → soft delete user)
    """
    serializer_class = UserMeSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.filter(is_active=True)

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        elif self.action == 'list':
            return [IsAdmin()]
        return super().get_permissions()

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(id=self.request.user.id)

    def create(self, request):
        """Create new user (public with limited roles, admin for any role)"""
        role = request.data.get('role')
        if not request.user.is_staff:  # Non-admin users
            if role not in [Role.ORPHANAGE, Role.DONOR, Role.VOLUNTEER]:
                return Response(
                    {"error": "Invalid role. Only Orphanage, Donor, or Volunteer roles allowed"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Update user (admin or self only)"""
        instance = self.get_object()
        if not request.user.is_staff and request.user.id != instance.id:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Soft delete user (self only)"""
        instance = self.get_object()
        if request.user.id != instance.id:
            return Response(status=status.HTTP_403_FORBIDDEN)
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
