"""Custom taggit models for user-specific tagging of UUID model items."""
from django.db import models
from taggit.models import ItemBase
from taggit.models import TagBase


class BmaTag(TagBase):
    """BMA uses this instead of the default taggit model to remove the unique=True constraint for tag name."""

    name = models.CharField(max_length=100, help_text="The tag")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """A string representation of a tag including weight if available."""
        weight = self.weight if hasattr(self, "weight") else 0
        return f"{self.name} ({weight})"


class TaggedFile(ItemBase):
    """BMA uses this instead of the default taggit through model to get the user relation."""

    content_object = models.ForeignKey("files.BaseFile", on_delete=models.CASCADE, related_name="taggings")
    tagger = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,  # delete users taggings when the tagger user is deleted
        related_name="taggings",
        help_text="The user who did the tagging.",
    )
    tag = models.ForeignKey(
        "tags.BmaTag",
        on_delete=models.CASCADE,  # delete taggings when a tag is deleted
        related_name="taggings",
        help_text="The tag.",
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        """A user can only tag a file with a tag once."""

        constraints = (models.UniqueConstraint(fields=["tagger", "tag", "content_object"], name="unique_user_tag"),)

    def __str__(self) -> str:
        """A string representation of a tagging."""
        return (
            f"Username {self.tagger.username} tagged {self.content_object.filetype} "
            f"uuid {self.content_object.uuid} with tag {self.tag.name}"
        )
