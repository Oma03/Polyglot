from django.urls import path
from .views import SignUpView, VerifyUser
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('verify-user/<token>', VerifyUser.as_view(), name='verify'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh')
]