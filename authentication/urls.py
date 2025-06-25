from django.urls import path
from .views import SignUpView, VerifyUser, ResendToken, LoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('verify-user/', VerifyUser.as_view(), name='verify'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('resend/', ResendToken.as_view(), name='resend'),
    path('login/', LoginView.as_view(), name='login'),
]