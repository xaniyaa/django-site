import logging

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from .models import File
from .utils import file_generate_upload_path, file_generate_name, file_generate_local_upload_url
from minio_integration.client import s3_generate_presigned_post
from authorization.models import CustomUser
import mimetypes
from typing import Any, Dict, Tuple


class FileUploadService:

    def __init__(self, user: CustomUser):
        self.user = user

    @transaction.atomic
    def start(self, *, file_name: str, file_type: str):
        file = File(
            original_file_name=file_name,
            file_name=file_generate_name(file_name),
            file_type=file_type,
            file=None
        )
        file.full_clean()
        file.save()

        upload_path = file_generate_upload_path(file, file.file_name)

        # спасибо мужику какому-то! а то ниже пиздец..

        file.file = file.file.field.attr_class(file, file.file.field, upload_path)
        file.save()

        presigned_data = {}

        if settings.FILE_UPLOAD_STORAGE == "s3":
            presigned_data = s3_generate_presigned_post(
                file_path=upload_path, file_type=file.file_type
            )
        else:
            presigned_data = {
                "url": file_generate_local_upload_url(file_id=str(file.id)),
            }

        return {"id": file.id, **presigned_data}

    @transaction.atomic
    def finish(self, *, file: File) -> File:
        file.upload_finished_at = timezone.now()
        file.full_clean()
        file.save()

        return file

    @transaction.atomic
    def upload_local(self, *, file: File, file_obj) -> File:
        file.file = file_obj
        file.full_clean()
        file.save()

        return file

# не сработало
class FileStandardUploadService:
    """
    This also serves as an example of a service class,
    which encapsulates 2 different behaviors (create & update) under a namespace.

    Meaning, we use the class here for:

    1. The namespace
    2. The ability to reuse `_infer_file_name_and_type` (which can also be an util)
    """

    def __init__(self, user: CustomUser, file_obj):
        self.user = user
        self.file_obj = file_obj
        print(self.file_obj)

    def _infer_file_name_and_type(self, file_name: str = "", file_type: str = "") -> Tuple[str, str]:
        if not file_name:
            file_name = self.file_obj.name

        if not file_type:
            guessed_file_type, encoding = mimetypes.guess_type(file_name)

            if guessed_file_type is None:
                file_type = ""
            else:
                file_type = guessed_file_type

        return file_name, file_type

    @transaction.atomic
    def create(self, file_name: str = "", file_type: str = "") -> File:

        file_name, file_type = self._infer_file_name_and_type(file_name, file_type)

        obj = File(
            file=self.file_obj,
            original_file_name=file_name,
            file_name=file_generate_name(file_name),
            file_type=file_type,
            uploaded_by=self.user,
            upload_finished_at=timezone.now(),
        )

        obj.full_clean()
        obj.save()

        return obj

    @transaction.atomic
    def update(self, file: File, file_name: str = "", file_type: str = "") -> File:

        file_name, file_type = self._infer_file_name_and_type(file_name, file_type)

        file.file = self.file_obj
        file.original_file_name = file_name
        file.file_name = file_generate_name(file_name)
        file.file_type = file_type
        file.uploaded_by = self.user
        file.upload_finished_at = timezone.now()

        file.full_clean()
        file.save()

        return file
