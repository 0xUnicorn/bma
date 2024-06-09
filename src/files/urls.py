"""URLs for the files app."""
from django.urls import include
from django.urls import path

from files.views import FileBrowserView
from files.views import FileDeleteView
from files.views import FileDetailView
from files.views import FileListView
from files.views import FileTagCreateView
from files.views import FileTagDeleteView
from files.views import FileTagDetailView
from files.views import FileTagListView
from files.views import FileUpdateView
from files.views import FileUploadView

app_name = "files"

urlpatterns = [
    path("", FileListView.as_view(), name="file_list"),
    path("jsbrowser/", FileBrowserView.as_view(), name="browse"),
    path("upload/", FileUploadView.as_view(), name="file_upload"),
    path(
        "<uuid:file_uuid>/",
        include(
            [
                path("", FileDetailView.as_view(), name="file_detail"),
                path("update/", FileUpdateView.as_view(), name="file_update"),
                path("delete/", FileDeleteView.as_view(), name="file_delete"),
                path(
                    "tags/",
                    include(
                        [
                            path("", FileTagListView.as_view(), name="file_tags"),
                            path("add/", FileTagCreateView.as_view(), name="file_tag_create"),
                            path(
                                "<str:tag_name>/",
                                include(
                                    [
                                        path("", FileTagDetailView.as_view(), name="file_tag_detail"),
                                        path("remove/", FileTagDeleteView.as_view(), name="file_tag_delete"),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ),
            ]
        ),
    ),
]
