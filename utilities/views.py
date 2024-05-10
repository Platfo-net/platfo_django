from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from utilities import s3_storage
from .serializers import UploadFileSerializer, UploadedFileSerializer


class BaseFileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = UploadFileSerializer
    read_serializer_class = UploadedFileSerializer
    s3_bucket = NotImplementedError()

    @extend_schema(
        operation_id='upload_file',
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'file': {
                        'type': 'string',
                        'format': 'binary'
                    }
                }
            }
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = self.request.FILES['file']
        uploaded_file_name = s3_storage.add_file_to_s3(file, self.s3_bucket)
        file_url = s3_storage.get_file_url(uploaded_file_name, self.s3_bucket)
        data = {
            'file_name': uploaded_file_name,
            'url': file_url
        }

        response_serializer = self.read_serializer_class(data=data)
        if response_serializer.is_valid():
            return Response(response_serializer.validated_data, status=status.HTTP_201_CREATED)
        else:
            return Response(response_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
