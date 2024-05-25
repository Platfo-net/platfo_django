from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from account.serializers import (UserLoginSerializer, ForgotPasswordSerializer, ChangePasswordSerializer,
                                 BaseUserSerializer, ActivateBySMSSerializer)
from account.utils import generate_random_code, generate_random_token, validate_code_and_token
from notification.enums import SMSNotificationSender
from utilities import cache
from utilities.http.response import OkResponse


class LoginPhoneNumberView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),  # noqa
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)


class ForgotPasswordView(APIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if cache.get_user_code(user.phone_number, user.phone_country_code):
            raise ValidationError('Reset password code has already been sent')

        token = generate_random_token(64)
        code = generate_random_code(4)
        cache.set_user_code(user.phone_number, user.phone_country_code, code, token)
        user.receive_sms(settings.SMS_IR_USER_RESET_PASSWORD_TEMPLATE_ID,
                         SMSNotificationSender.RESET_PASSWORD.value, code)
        return Response(data={'token': token}, status=status.HTTP_201_CREATED)


class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        cached_data = cache.get_user_code(user.phone_number, user.phone_country_code)
        if not cached_data:
            raise ValidationError('Invalid code or token')
        validate_code_and_token(cached_data, serializer.validated_data)

        user.password = make_password(serializer.validated_data['password'])
        user.save(update_fields=['password'])
        cache.remove_user_code(user.phone_number, user.phone_country_code)
        return OkResponse()


class ActivationCodeBySMSView(APIView):
    serializer_class = BaseUserSerializer

    def post(self, request):
        serializer = BaseUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user.is_active:
            raise ValidationError('User is already active')

        cached_data = cache.get_user_code(user.phone_number, user.phone_country_code)
        if cached_data:
            raise ValidationError('Activation code has already been sent')

        token = generate_random_token(64)
        code = generate_random_code(5)
        cache.set_user_code(user.phone_number, user.phone_country_code, code, token)
        user.receive_sms(settings.SMS_IR_USER_ACTIVATION_TEMPLATE_ID,
                         SMSNotificationSender.USER_ACTIVATION.value, code)

        return Response(data={'token': token}, status=status.HTTP_201_CREATED)


class ActivateBySMSView(APIView):
    serializer_class = ActivateBySMSSerializer

    def post(self, request):
        serializer = ActivateBySMSSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        cached_data = cache.get_user_code(user.phone_number, user.phone_country_code)
        if not cached_data:
            raise ValidationError('Invalid code or token')
        validate_code_and_token(cached_data, serializer.validated_data)

        user.is_active = True
        user.save(update_fields=['is_active'])

        cache.remove_user_code(user.phone_number, user.phone_country_code)
        return OkResponse()
