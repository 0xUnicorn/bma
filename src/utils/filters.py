"""The shared filters used in the files and albums API endpoints."""
from django.db import models
from ninja import Schema


class SortingChoices(models.TextChoices):
    """The sorting options for files and albums."""

    title_asc = ("title_asc", "Title (ascending)")
    title_desc = ("title_desc", "Title (descending)")
    description_asc = ("description_asc", "Description (ascending)")
    description_desc = ("description_desc", "Description (descending)")
    created_asc = ("created_asc", "Created (ascending)")
    created_desc = ("created_desc", "Created (descending)")
    updated_asc = ("updated_asc", "Updated (ascending)")
    updated_desc = ("updated_desc", "Updated (descending)")


class ListFilters(Schema):
    """Filters shared between the file_list and album_list endpoints."""

    limit: int = 100
    offset: int | None = None
    search: str | None = None
    sorting: SortingChoices | None = None
