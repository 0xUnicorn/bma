"""CBV mixins for album based views."""

from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from .models import Album


class AlbumViewMixin:
    """A mixin shared by views working on albums, sets self.album from album_uuid in url kwargs."""

    def setup(self, request: HttpRequest, *args: str, **kwargs: dict[str, str]) -> None:
        """Get album object from url."""
        super().setup(request, *args, **kwargs)  # type: ignore[misc]
        self.album = get_object_or_404(Album.bmanager.all(), uuid=kwargs["album_uuid"])

    def get_context_data(self, **kwargs: dict[str, str]) -> dict[str, str]:
        """Add file to context."""
        context = super().get_context_data(**kwargs)  # type: ignore[misc]
        context["album"] = self.album
        return context  # type: ignore[no-any-return]
