from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)
from .views import (
    UserRegisterAPIView,
    MyProfileAPIView,
    ResetPassword,
    PasswordTokenCheckView,
    SetPasswordView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('api/register/', UserRegisterAPIView.as_view(), name='register'),
    path('api/profile/', MyProfileAPIView.as_view(), name='profile'),
    path('api/reset/passwd/', ResetPassword.as_view(), name='reset'),
    path('api/check/passwd/<str:uidb64>/<str:token>/', PasswordTokenCheckView.as_view(), name='check_passwd'),
    path('api/set/passwd/', SetPasswordView.as_view(), name='set_new_passwd'),
]

