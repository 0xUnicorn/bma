"""This module defines the table used to show files."""
import django_tables2 as tables
from albums.models import Album
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe

from .models import BaseFile


class FileTable(tables.Table):
    """Defines the django-tables2 used to show files."""

    selection = tables.CheckBoxColumn(accessor="pk", orderable=False)
    uuid = tables.Column(linkify=True)
    albums = tables.Column(verbose_name="Albums")

    def render_albums(self, record: BaseFile) -> str:
        """Render albums as a list of links."""
        output = ""
        for album in Album.objects.filter(
            memberships__basefile__pk__contains=record.pk, memberships__period__contains=timezone.now()
        ):
            output += (
                '<a href="' + reverse("albums:album_detail", kwargs={"pk": album.pk}) + '">' + album.title + "</a><br>"
            )
        return mark_safe(output)  # noqa: S308

    def render_tags(self, record: BaseFile) -> str:
        """Render tags in a taggy way."""
        output = ""
        for tag in record.tags.weighted.all():
            output += f'<span class="badge bg-secondary">{tag}</span> '
        return mark_safe(output)  # noqa: S308

    class Meta:
        """Define model, template, fields."""

        model = BaseFile
        template_name = "django_tables2/bootstrap.html"
        fields = (
            "selection",
            "uuid",
            "title",
            "albums",
            "attribution",
            "uploader",
            "license",
            "file_size",
            "tags",
            "approved",
            "published",
            "deleted",
        )
