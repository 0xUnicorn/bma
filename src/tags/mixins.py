"""CBV mixins for tag related views."""

from django.http import HttpRequest
from django.shortcuts import get_object_or_404


class TagViewMixin:
    """A mixin shared by views working on tags, sets self.tag from tag_name in url kwargs."""

    def setup(self, request: HttpRequest, *args: str, **kwargs: dict[str, str]) -> None:
        """Get tag object from url. Requires self.file to be set."""
        self.tag = get_object_or_404(self.file.tags.weighted.all(), name=kwargs["tag_name"])  # type: ignore[attr-defined]
        super().setup(request, **kwargs)  # type: ignore[misc]
