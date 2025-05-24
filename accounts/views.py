from rest_framework import  viewsets, permissions, status,generics
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

class UserListView(generics.ListAPIView):
    """GET /users/ (admin → list users)"""
    serializer_class = UserMeSerializer
    permission_classes = [IsAdmin]
    queryset = User.objects.filter(is_active=True)


class UserCreateView(generics.CreateAPIView):
    """POST /users/ (anonymous → create user with limited roles, admin → create any role)"""
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        role = request.data.get('role')
        if not request.user.is_staff:  # Non-admin users
            if role not in [Role.ORPHANAGE, Role.DONOR, Role.VOLUNTEER]:
                return Response(
                    {"error": "Invalid role. Only Orphanage, Donor, or Volunteer roles allowed"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDetailView(generics.ListAPIView):
    """GET /users/me/ (self → user details)"""
    serializer_class = UserMeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class UserUpdateView(generics.UpdateAPIView):
    """PATCH /users/me/ (self → update user)"""
    serializer_class = UserMeSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return self.request.user
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
    


class UserDeleteView(generics.DestroyAPIView):
    """DELETE /users/me/ (self → soft delete user)"""
    serializer_class = UserMeSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.filter(is_active=True)

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
