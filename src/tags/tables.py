"""This module defines the table used to show tags."""
import django_tables2 as tables

from .models import BmaTag
from .models import TaggedFile


class TagTable(tables.Table):
    """Defines the django-tables2 used to show tags."""

    class Meta:
        """Define model, template, fields."""

        model = BmaTag
        template_name = "django_tables2/bootstrap.html"
        fields = (
            "name",
            "weight",
            "created",
            "taggers",
        )


class TaggingTable(tables.Table):
    """Defines the django-tables2 used to show taggings."""

    tagger = tables.Column(linkify=True)

    class Meta:
        """Define model, template, fields."""

        model = TaggedFile
        template_name = "django_tables2/bootstrap.html"
        fields = (
            "tagger",
            "tag",
            "created",
        )
