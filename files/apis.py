from django.shortcuts import get_object_or_404

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from files.models import File
from files.services import (
    FileUploadService,
    FileStandardUploadService
)

from api.mixins import ApiAuthMixin


class FileUploadApi(ApiAuthMixin, APIView):

    class InputSerializer(serializers.Serializer):
        file_name = serializers.CharField()
        file_type = serializers.CharField()

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = FileUploadService(request.user)
        presigned_data = service.start(**serializer.validated_data)

        return Response(data=presigned_data)


class FileUploadLocalApi(ApiAuthMixin, APIView):
    def post(self, request, file_id):
        file = get_object_or_404(File, id=file_id)

        file_obj = request.FILES["file"]

        service = FileUploadService(request.user)
        file = service.upload_local(file=file, file_obj=file_obj)

        return Response({"id": file.id})


# class FileStandardUploadApi((ApiAuthMixin, APIView):
#     def post(self, request):
#         service = FileStandardUploadService(user=request.user, file_obj=request.FILES.get('file'))
#         file = service.create()
#
#         return Response(data={"id": file.id}, status=status.HTTP_201_CREATED)