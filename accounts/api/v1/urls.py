from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from accounts.api.v1.views import LoginView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token-refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token-verify', TokenVerifyView.as_view(), name='token_verify'),
]