from core import settings
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import User, Token
from .utils import handle_exceptions, send_verification_email
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import EmailValidator
from rest_framework.exceptions import ValidationError
from django.utils import timezone


RETURN_RESPONSE = settings.RESPONSE_TEMPLATE

# Create your views here.

# Sign up View
# METHOD: POST
# BODY: email, password


class SignUpView(APIView):

    permission_classes = [AllowAny]

    @handle_exceptions
    def post(self, request):
        # Receive email and password from user input
        email = request.data['email']
        password = request.data['password']

        #  Check if email already exists
        if User.objects.filter(email=email):
            RETURN_RESPONSE['status'] = False
            RETURN_RESPONSE['message'] = "Email already in use"
            RETURN_RESPONSE['data'] = {}
            return Response(RETURN_RESPONSE, status=status.HTTP_400_BAD_REQUEST)

        try:
            validator = EmailValidator()
            validator(email)
        except ValidationError:
            RETURN_RESPONSE['status'] = False
            RETURN_RESPONSE['message'] = "Invalid email, please try again"
            RETURN_RESPONSE['data'] = {}
            return Response(RETURN_RESPONSE, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(email=email, password=password)
        user.save()

        verify = send_verification_email(email)

        RETURN_RESPONSE['status'] = True
        RETURN_RESPONSE['message'] = "User created successfully, please check your email to get verified!"
        RETURN_RESPONSE['data'] = {
            "email" : email,
            "verify" : verify
        }
        return Response(RETURN_RESPONSE, status=status.HTTP_200_OK)

# Verify User View
# METHOD : get
# Body: email, token


class VerifyUser(APIView):
    permission_classes = [AllowAny]

    @handle_exceptions
    def get(self, request):
        token = request.GET.get('token')
        if not token:
            RETURN_RESPONSE['status'] = False
            RETURN_RESPONSE['message'] = 'No token provided'
            RETURN_RESPONSE['data'] = {}
            return Response(RETURN_RESPONSE, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        user_token = Token.objects.filter(user=user, token=token)

        if user_token.expires_at < timezone.now():
            RETURN_RESPONSE['status'] = False
            RETURN_RESPONSE['message'] = "Token is expired"
            RETURN_RESPONSE['data'] = {}
            return Response(RETURN_RESPONSE, status=status.HTTP_400_BAD_REQUEST)

        user.verified = True
        user.save()
        RETURN_RESPONSE['status'] = True
        RETURN_RESPONSE['message'] = "Email verified successfully"
        RETURN_RESPONSE['data'] = {}

        return Response(RETURN_RESPONSE, status=status.HTTP_200_OK)