"""CBV mixins for file based views."""

from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from .models import BaseFile


class FileViewMixin:
    """A mixin shared by views working on files, sets self.file from file_uuid in url kwargs."""

    def setup(self, request: HttpRequest, *args: str, **kwargs: dict[str, str]) -> None:
        """Get file object from url."""
        self.file = get_object_or_404(BaseFile.bmanager.get_permitted(user=self.request.user), uuid=kwargs["file_uuid"])  # type: ignore[attr-defined]
        super().setup(request, **kwargs)  # type: ignore[misc]
