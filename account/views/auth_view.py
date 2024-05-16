from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from account.serializers import (UserLoginSerializer, ForgotPasswordSerializer)
from account.utils import generate_random_code, generate_random_token, set_user_reset_password_code, \
    get_user_reset_password_code
from notification.enums import SMSNotificationSender


class LoginPhoneNumberView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token), # noqa
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)


class ForgotPasswordView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if get_user_reset_password_code(user.phone_number, user.phone_country_code):
            raise ValidationError('Reset password code has already been sent')

        token = generate_random_token(64)
        code = generate_random_code(4)
        set_user_reset_password_code(user.phone_number, user.phone_country_code, code, token)
        user.receive_sms(settings.SMS_IR_USER_RESET_PASSWORD_TEMPLATE_ID,
                         SMSNotificationSender.RESET_PASSWORD.value, code)
        return Response(data={'token': token}, status=status.HTTP_201_CREATED)
