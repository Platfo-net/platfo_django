from rest_framework.views import APIView

from account.serializers import UserRegisterByPhoneNumberSerializer
from utilities.http.response import OkResponse


class RegisterByPhoneNumberView(APIView):
    serializer_class = UserRegisterByPhoneNumberSerializer

    def post(self, request):
        serializer = UserRegisterByPhoneNumberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return OkResponse()
