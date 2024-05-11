"""ModelAdmin for the Album model."""
from django.contrib import admin

from .models import Album
from .models import AlbumMember


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin[Album]):
    """ModelAdmin for the Album model."""

    list_display = (
        "uuid",
        "owner",
        "created",
        "updated",
        "title",
        "description",
        "description",
    )
    list_filter = ("owner",)

@admin.register(AlbumMember)
class AlbumMemberAdmin(admin.ModelAdmin):
    """ModelAdmin for the Album model."""

    list_display = (
        "uuid",
        "basefile",
        "album",
        "period",
    )

