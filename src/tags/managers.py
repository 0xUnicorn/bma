"""Custom taggit manager to include tagging user in lookup_kwargs, which is used to find through relations."""
from typing import Any

from django.db import models
from taggit.managers import _TaggableManager
from users.models import UserType

from .models import BmaTag


class BMATagManager(_TaggableManager):
    """Custom taggit manager to include tagging user in lookup_kwargs, which is used to find through relations."""

    def _lookup_kwargs(self) -> dict[str, str | UserType]:
        """Override _lookup_kwargs to include the tagger/user in the lookup."""
        kwargs = self.through.lookup_kwargs(self.instance)
        kwargs["tagger"] = self.tagger
        return kwargs  # type: ignore[no-any-return]

    def add(self, *args: str, tagger: UserType, **kwargs: Any) -> None:  # noqa: ANN401
        """Make sure tagger is available for _lookup_kwargs when doing .add."""
        self.tagger = tagger
        super().add(*args, **kwargs)

    def set(self, *args: str, tagger: UserType, **kwargs: Any) -> None:  # noqa: ANN401
        """Make sure tagger is available for _lookup_kwargs when doing .set."""
        self.tagger = tagger
        super().set(*args, **kwargs)

    def remove(self, *args: str, tagger: UserType) -> None:
        """Make sure tagger is available for _lookup_kwargs when doing .remove."""
        self.tagger = tagger
        super().remove(*args)

    def clear(self, tagger: UserType) -> None:
        """Make sure tagger is available for _lookup_kwargs when doing .clear."""
        self.tagger = tagger
        super().clear()

    def similar_objects(self, tagger: UserType) -> models.QuerySet[Any]:
        """Make sure tagger is available for _lookup_kwargs when doing .similar_objects."""
        self.tagger = tagger
        return super().similar_objects()  # type: ignore[no-any-return]

    @property
    def weighted(self) -> models.QuerySet[Any]:
        """Annotate tags with weights and order with heaviest first and then alphabetically."""
        # maybe figure out a fancier way to include a list of taggings per tag
        return self.annotate(  # type: ignore[no-any-return]
            weight=models.Count("name"),
        ).order_by("-weight", "name", "created")

    @property
    def weighted_list(self) -> list[BmaTag]:
        """Add tagger_uuids and instance_taggings and return tags a list."""
        tags = self.weighted.all()
        taggings = self.instance.taggings.all()
        taglist = []
        for tag in tags:
            tag.tagger_uuids = taggings.filter(tag=tag).values_list("tagger__uuid", flat=True)
            tag.instance_taggings = taggings.filter(tag=tag)
            taglist.append(tag)
        return taglist

    def add_user_tags(self, *tags: str, user: UserType) -> None:
        """Convenience method to add tag(s) for a user."""
        self.add(*tags, tagger=user, through_defaults={"tagger": user})
