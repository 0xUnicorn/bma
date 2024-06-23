"""CBV mixins used throughout the project."""
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest


class CuratorGroupRequiredMixin:
    """This mixin makes the view only accessible by users in the curators group."""

    def setup(self, request: HttpRequest, *args: str, **kwargs: dict[str, str]) -> None:
        """Check for membership of settings.BMA_CURATOR_GROUP_NAME and raise PermissionDenied if needed."""
        if settings.BMA_CURATOR_GROUP_NAME not in request.user.cached_groups:  # type: ignore[union-attr]
            raise PermissionDenied
        super().setup(request, *args, **kwargs)  # type: ignore[misc]
