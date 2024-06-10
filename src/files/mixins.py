"""CBV mixins for file based views."""

from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from .models import BaseFile


class FileViewMixin:
    """A mixin shared by views working on files, sets self.file from file_uuid in url kwargs."""

    def setup(self, request: HttpRequest, *args: str, **kwargs: dict[str, str]) -> None:
        """Get file object from url."""
        super().setup(request, *args, **kwargs)  # type: ignore[misc]
        self.file = get_object_or_404(BaseFile.bmanager.get_permitted(user=self.request.user), uuid=kwargs["file_uuid"])  # type: ignore[attr-defined]

    def get_context_data(self, **kwargs: dict[str, str]) -> dict[str, str]:
        """Add file to context."""
        context = super().get_context_data(**kwargs)  # type: ignore[misc]
        context["file"] = self.file
        return context  # type: ignore[no-any-return]
