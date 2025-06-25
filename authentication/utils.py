import random
from django.core.mail import send_mail
from .models import User, Token
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
    user_token = Token.objects.create(email=email, token=token, expires_at=timezone.now() + timedelta(hours=1))
    user_token.save()

    verify_url = f"http://localhost:8000/authentication/verify-user/?token={token}"
    # Send email
    print(send_mail(
        'Verify your email',
        f'Click on this link to verify your email: {verify_url}',
        'admin@gmail.com',
        [email],
        fail_silently=False,
    ))
