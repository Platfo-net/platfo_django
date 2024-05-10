from django.conf import settings
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import User
from account.serializers import (UserRegisterByPhoneNumberSerializer,
                                 UpdateUserSerializer, UpdateUserPasswordSerializer,
                                 UserSerializer)
from utilities.http.response import OkResponse
from utilities.views import BaseFileUploadView


class RegisterByPhoneNumberView(APIView):
    serializer_class = UserRegisterByPhoneNumberSerializer

    def post(self, request):
        serializer = UserRegisterByPhoneNumberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return OkResponse()


class UpdateUserView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangeUserPasswordView(UpdateAPIView):
    serializer_class = UpdateUserPasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class GetUserMeView(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UploadUserProfileImageView(BaseFileUploadView):
    permission_classes = [IsAuthenticated]
    s3_bucket = settings.S3_USER_PROFILE_BUCKET
