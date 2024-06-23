"""Managers for the Album model."""
from django.db import models
from django.db.models import Count
from django.db.models import Prefetch
from django.db.models import Q
from django.utils import timezone
from files.models import BaseFile


class AlbumManager(models.Manager):  # type: ignore[type-arg]
    """This is the default manager for the Album model."""

    def get_queryset(self):  # type: ignore[no-untyped-def]  # noqa: ANN201
        """Annotations and prefetches for the Album model."""
        qs = super().get_queryset()

        # queries to count past, present, and future memberships of each album
        active_memberships = Count("memberships", filter=Q(memberships__period__contains=timezone.now()), distinct=True)
        historic_memberships = Count("memberships", filter=Q(memberships__period__endswith__lt=timezone.now()))
        future_memberships = Count("memberships", filter=Q(memberships__period__startswith__gt=timezone.now()))

        return (
            qs.annotate(
                active_memberships=active_memberships,
                historic_memberships=historic_memberships,
                future_memberships=future_memberships,
            )
            .select_related("owner")
            .prefetch_related("user_permissions__user")
            .prefetch_related("user_permissions__permission")
            .prefetch_related("group_permissions__group")
            .prefetch_related("group_permissions__permission")
            .prefetch_related(
                Prefetch(
                    "files",
                    queryset=BaseFile.objects.filter(
                        memberships__period__contains=timezone.now(),
                    ).distinct(),
                    to_attr="active_files_list",
                ),
            )
            .prefetch_related("hits")
            .annotate(hitcount=Count("hits", distinct=True))
        )
