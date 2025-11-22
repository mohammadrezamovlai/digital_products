from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AppUserViewSet, RegisterView,AppUserTokenView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView


router = DefaultRouter()
router.register(r'users', AppUserViewSet, basename='appuser')

urlpatterns = router.urls + [
    path('register/', RegisterView.as_view(), name='appuser-register'),
    path("appuser/token/", AppUserTokenView.as_view(), name="appuser_token"),

    
]

