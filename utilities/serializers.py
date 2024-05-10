from rest_framework import serializers
from rest_framework.serializers import Serializer, FileField


class UploadFileSerializer(Serializer):
    file = FileField()

    class Meta:
        fields = ['file']


class UploadedFileSerializer(serializers.Serializer):
    file_name = serializers.CharField()
    url = serializers.CharField()
