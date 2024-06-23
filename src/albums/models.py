"""The album model."""
import logging
import uuid
from typing import TypeAlias

from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import DateTimeRangeField
from django.contrib.postgres.fields import RangeOperators
from django.db import models
from django.db.models import F
from django.urls import reverse
from django.utils import timezone
from files.models import BaseFile
from guardian.models import GroupObjectPermissionBase
from guardian.models import UserObjectPermissionBase
from guardian.shortcuts import assign_perm
from psycopg2.extras import DateTimeTZRange
from users.sentinel import get_sentinel_user

from .managers import AlbumManager

logger = logging.getLogger("bma")


class Album(models.Model):  # type: ignore[django-manager-missing]
    """The Album model is used to group files (from all users, like a spotify playlist)."""

    objects = models.Manager()

    bmanager = AlbumManager()

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="The unique ID (UUID4) of this object.",
    )

    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET(get_sentinel_user),
        related_name="albums",
        help_text="The creator of this album.",
    )

    created = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time when this object was first created.",
    )

    updated = models.DateTimeField(
        auto_now=True,
        help_text="The date and time when this object was last updated.",
    )

    title = models.CharField(
        max_length=255,
        blank=False,
        help_text="The title of this album. Required.",
    )

    description = models.TextField(
        blank=True,
        help_text="The description of this album. Optional. Supports markdown.",
    )

    files = models.ManyToManyField(
        BaseFile,
        through="AlbumMember",
        related_name="albums",
    )

    class Meta:
        """Order by created date initially."""

        ordering = ("created",)

    def __str__(self) -> str:
        """The string representation of an album."""
        return f"{self.title} ({self.uuid})"

    def get_absolute_url(self) -> str:
        """The detail url for the album."""
        return reverse("albums:album_detail", kwargs={"album_uuid": self.pk})

    def add_members(self, *file_uuids: str) -> None:
        """Create new memberships for the file_uuids."""
        # maybe add all at once?
        for u in file_uuids:
            AlbumMember.objects.get_or_create(
                basefile_id=u,
                album=self,
                period__startswith__lte=timezone.now(),
                period__endswith=None,
            )

    def remove_members(self, *file_uuids: str) -> None:
        """End the memberships for the file_uuids."""
        # maybe do this as one query with F() and .update()
        for membership in self.memberships.filter(basefile__uuid__in=file_uuids, period__endswith__isnull=True):
            membership.period = DateTimeTZRange(membership.period.lower, timezone.now())
            membership.save(update_fields=["period"])

    def add_initial_permissions(self) -> None:
        """Add initial permissions for newly created albums."""
        assign_perm("change_album", self.owner, self)

    @property
    def active_files(self) -> models.QuerySet["BaseFile"]:
        """Return a qs of currently active files, for use when the manager is not available."""
        return self.files.filter(memberships__period__contains=timezone.now())

    def update_members(self, *file_uuids: str, replace: bool) -> None:
        """Update active album members to file_uuids, adding/removing or replacing as needed."""
        current_uuids = set(self.active_files.values_list("uuid", flat=True))
        if replace:  # PUT
            # first end all current memberships
            self.remove_members(*current_uuids)
            # add the new memberships
            self.add_members(*file_uuids)
        else:  # PATCH
            # we are updating the list of files
            self.remove_members(*current_uuids.difference(file_uuids))
            # get the list of files to be added to the album
            add_uuids = set(file_uuids).difference(current_uuids)
            self.add_members(*add_uuids)


def from_now_to_forever() -> DateTimeTZRange:
    """Return a DateTimeTZRange starting now and never stopping."""
    return DateTimeTZRange(timezone.now(), None)


class ActiveAlbumMemberManager(models.Manager):  # type: ignore[type-arg]
    """Filter away inactive album members."""

    def get_queryset(self):  # type: ignore[no-untyped-def]  # noqa: ANN201
        """Only get active memberships."""
        return super().get_queryset().filter(memberships__period__contains=timezone.now())


class AlbumMember(models.Model):
    """The through model linking Albums and files."""

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="The unique ID (UUID4) of this object.",
    )

    # if the basefile object gets deleted from database also delete the AlbumMember
    basefile = models.ForeignKey(BaseFile, related_name="memberships", on_delete=models.CASCADE)

    # if the album object gets deleted from database also delete the AlbumMembers
    album = models.ForeignKey(Album, related_name="memberships", on_delete=models.CASCADE)

    period = DateTimeRangeField(
        default=from_now_to_forever,
        help_text="The time range of this album membership. End time can be blank.",
    )

    objects = models.Manager()  # Default Manager
    active_members = ActiveAlbumMemberManager()

    class Meta:
        """Make sure a file can only be a member of an album once at any given point in time."""

        constraints = (
            # we do not want overlapping memberships
            ExclusionConstraint(
                name="prevent_membership_overlaps",
                expressions=[
                    (F("basefile"), RangeOperators.EQUAL),
                    (F("album"), RangeOperators.EQUAL),
                    ("period", RangeOperators.OVERLAPS),
                ],
            ),
        )

    def __str__(self) -> str:
        """The string representation of an album member file."""
        if self.period.upper is not None:
            return (
                f"{self.basefile.uuid} was in album {self.album.uuid} from {self.period.lower} to {self.period.upper}"
            )
        return f"{self.basefile.uuid} is in album {self.album.uuid} from {self.period.lower}"


class AlbumUserObjectPermission(UserObjectPermissionBase):
    """Use a direct (non-generic) FK for user album permissions in guardian."""

    content_object = models.ForeignKey("albums.Album", related_name="user_permissions", on_delete=models.CASCADE)


class AlbumGroupObjectPermission(GroupObjectPermissionBase):
    """Use a direct (non-generic) FK for group album permissions in guardian."""

    content_object = models.ForeignKey("albums.Album", related_name="group_permissions", on_delete=models.CASCADE)


AlbumType: TypeAlias = Album
