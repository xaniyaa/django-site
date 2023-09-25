from .apis import (
    FileDirectUploadLocalApi,
    FileDirectUploadStartApi,
    FileDirectUploadFinishApi,
    FileStandardUploadApi,
)
from django.urls.conf import path, include

urlpatterns = [
    path(
        "upload/",
        include(
            (
                [
                    path("standard/", FileStandardUploadApi.as_view(), name="standard"),
                    path(
                        "direct/",
                        include(
                            (
                                [
                                    path("start/", FileDirectUploadStartApi.as_view(), name="start"),
                                    path("finish/", FileDirectUploadFinishApi.as_view(), name="finish"),
                                    path("local/<str:file_id>/", FileDirectUploadLocalApi.as_view(), name="local"),
                                ],
                                "direct",
                            )
                        ),
                    ),
                ],
                "upload",
            )
        ),
    )]
