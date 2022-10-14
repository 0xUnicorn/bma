# Generated by Django 4.1.1 on 2022-10-09 18:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BaseFile",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text="The unique ID (UUID4) of this object.",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="The date and time when this object was first created.",
                    ),
                ),
                (
                    "updated",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="The date and time when this object was last updated.",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="The title of this work. Required. Defaults to the original uploaded filename.",
                        max_length=255,
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="The description of this work. Optional. Supports markdown.",
                    ),
                ),
                (
                    "source",
                    models.URLField(
                        help_text="The URL to the original source of this work. Leave blank to consider the BMA URL the original source."
                    ),
                ),
                (
                    "license",
                    models.CharField(
                        choices=[
                            ("CC_ZERO_1_0", "Creative Commons CC0 1.0 Universal"),
                            (
                                "CC_BY_4_0",
                                "Creative Commons Attribution 4.0 International",
                            ),
                            (
                                "CC_BY_SA_4_0",
                                "Creative Commons Attribution-ShareAlike 4.0 International",
                            ),
                        ],
                        help_text="The license for this file.",
                        max_length=255,
                    ),
                ),
                (
                    "attribution",
                    models.CharField(
                        help_text="The attribution text for this file. This is usually the real name or handle of the author(s) or licensor of the file.",
                        max_length=255,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING_MODERATION", "Pending Moderation"),
                            ("UNPUBLISHED", "Unpublished"),
                            ("PUBLISHED", "Published"),
                            ("PENDING_DELETION", "Pending Deletion"),
                        ],
                        default="PENDING_MODERATION",
                        help_text="The status of this file. Only published files are visible on the public website.",
                        max_length=20,
                    ),
                ),
                (
                    "original_filename",
                    models.CharField(
                        help_text="The original (uploaded) filename.", max_length=255
                    ),
                ),
            ],
            options={
                "ordering": ["created"],
                "permissions": (
                    ("approve_basefile", "Approve file"),
                    ("unpublish_basefile", "Unpublish file"),
                    ("publish_basefile", "Publish file"),
                ),
            },
        ),
    ]
