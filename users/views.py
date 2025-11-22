from rest_framework import generics, viewsets, permissions
from .models import AppUser
from .serializers import AppUserSerializer, RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.hashers import check_password

from rest_framework_simplejwt.tokens import RefreshToken




class AppUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer
    permission_classes = [permissions.IsAdminUser]


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class AppUserTokenView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user = AppUser.objects.get(username=username)
        except AppUser.DoesNotExist:
            return Response({"detail": "User not found"}, status=404)

        if not user.check_password(password):
            return Response({"detail": "Incorrect password"}, status=400)

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })
