from pathlib import Path

from django.db import models
from taggit.managers import TaggableManager

from utils.models import MediaBaseModel
from utils.models import UUIDTaggedItem


def get_audio_upload_path(instance, filename):
    """Return the upload path for this audio file."""
    return Path(
        f"audios/user_{instance.gallery.owner.id}/gallery_{instance.gallery.uuid}/audio_{instance.uuid}.{Path(filename).suffix.lower()}",
    )


class Audio(MediaBaseModel):
    """The Audio model."""

    original_filename = models.CharField(
        max_length=255,
        help_text="The original (uploaded) filename.",
    )

    audio = models.FileField(upload_to=get_audio_upload_path)

    tags = TaggableManager(
        through=UUIDTaggedItem,
        help_text="The tags for this audio file",
    )
