import random
from django.core.mail import send_mail
from .models import Token, User
from django.utils.decorators import wraps
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import secrets
from django.utils import timezone
from datetime import timedelta

RETURN_RESPONSE = settings.RESPONSE_TEMPLATE


def handle_exceptions(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        try:
            return view_func(self, request, *args, **kwargs)
        except Exception as e:
            RETURN_RESPONSE['status'] = False
            RETURN_RESPONSE['message'] = str(e)
            print(e)
            return Response(RETURN_RESPONSE, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return wrapper

def send_verification_email(email):
    # Generate token
    token = secrets.token_urlsafe(32)
    user = User.objects.get(email=email)
    user_token = Token.objects.create(user=user, token=token, expires_at=timezone.now() + timedelta(hours=1))
    user_token.save()

    verify_url = f"http://localhost:80000/api/verify-email/?token={token}"
    # Send email
    send_mail(
        'Verify your email',
        f'Click on this link to verify your email {verify_url}',
        'admin@gmail.com',
        [email],
        fail_silently=False,
    )

# def generate_and_send_reset_otp(email):
#     # Generate 6-digit OTP
#     otp = str(random.randint(100000, 999999))
#     user = User.objects.get(email=email)
#
#     # Save OTP in the database
#     ResetOTP.objects.create(user=user, otp=otp)
#
#     #Send email
#     send_mail(
#         'Your OTP Code',
#         f'Your OTP to reset your password is {otp}. It will expire in 5 minutes.',
#         'admin@gmail.com',
#         [email],
#         fail_silently=False,
#     )