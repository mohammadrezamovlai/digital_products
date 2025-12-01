# from rest_framework import generics, viewsets, permissions
# from .models import AppUser
# from .serializers import AppUserSerializer, RegisterSerializer
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# from django.contrib.auth.hashers import check_password

# from rest_framework_simplejwt.tokens import RefreshToken




# class AppUserViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = AppUser.objects.all()
#     serializer_class = AppUserSerializer
#     permission_classes = [permissions.IsAdminUser]


# class RegisterView(generics.CreateAPIView):
#     serializer_class = RegisterSerializer
#     permission_classes = [permissions.AllowAny]

# class AppUserTokenView(APIView):
#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")

#         try:
#             user = AppUser.objects.get(username=username)
#         except AppUser.DoesNotExist:
#             return Response({"detail": "User not found"}, status=404)

#         if not user.check_password(password):
#             return Response({"detail": "Incorrect password"}, status=400)

#         refresh = RefreshToken.for_user(user)

#         return Response({
#             "refresh": str(refresh),
#             "access": str(refresh.access_token),
#         })
import uuid
import random

from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from .models import User, Device
from rest_framework import generics,permissions

# class RegisterView(APIView):

#     def post(self, request):
#         phone_number = request.data.get('phone_number')

#         if not phone_number:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#         try:
#             user = User.objects.get(phone_number=phone_number)
#             # return Response({'detail': 'User already registered!'},
#             #                 status=status.HTTP_400_BAD_REQUEST)
#         except User.DoesNotExist:
#             user = User.objects.create_user(phone_number=phone_number)

#         # user, created = User.objects.get_or_create(phone_number=phone_number)

#         device = Device.objects.create(user=user)

#         code = random.randint(10000, 99999)

#         # send message (sms or email)
#         # cache
#         cache.set(str(phone_number), code, 2 * 60)

#         return Response({'code': code})

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save() 

        # ایجاد Device
        Device.objects.create(user=user)

        # تولید کد OTP
        code = random.randint(10000, 99999)
        cache.set(str(user.phone_number), code, 2 * 60) 

        return Response({
            'code': code,
            'user': serializer.data  # 
        }, status=status.HTTP_201_CREATED)
    

class GetTokenView(APIView):

    def post(self, request):
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')

        cached_code = cache.get(str(phone_number))

        if code != cached_code:
            return Response(status=status.HTTP_403_FORBIDDEN)

        token = str(uuid.uuid4())

        return Response({'token': token})