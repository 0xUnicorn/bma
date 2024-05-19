"""The filters used for the file_list endpoint."""
import uuid
from typing import ClassVar

import django_filters
from django.db.models import QuerySet
from django.utils import timezone
from utils.filters import ListFilters

from .models import BaseFile
from .models import FileTypeChoices
from .models import LicenseChoices
from .models import StatusChoices


class FileFilters(ListFilters):
    """The filters used for the file_list endpoint."""

    albums: list[uuid.UUID] | None = None
    statuses: list[StatusChoices] | None = None
    uploaders: list[uuid.UUID] | None = None
    licenses: list[LicenseChoices] | None = None
    filetypes: list[FileTypeChoices] | None = None
    size: int | None = None
    size_lt: int | None = None
    size_gt: int | None = None
    attribution: str | None = None


class FileFilter(django_filters.FilterSet):
    """The main django-filters filter used in views showing files."""

    albums = django_filters.filters.UUIDFilter(field_name="albums", method="filter_albums")
    not_albums = django_filters.filters.UUIDFilter(field_name="albums", method="filter_albums", exclude=True)

    def filter_albums(self, queryset: QuerySet[BaseFile], name: str, value: str) -> QuerySet[BaseFile]:
        """When filtering for albums only consider currently active memberships."""
        return queryset.filter(memberships__album__in=[value], memberships__period__contains=timezone.now())

    class Meta:
        """Set model and fields."""

        model = BaseFile
        fields: ClassVar[dict[str, list[str]]] = {
            "albums": ["exact"],
            "attribution": ["exact", "icontains"],
            "status": ["exact"],
            "uploader": ["exact"],
            "license": ["exact"],
            "file_size": ["exact", "lt", "gt"],
        }
