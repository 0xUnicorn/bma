# Generated by Django 5.0.6 on 2024-06-23 07:03

import albums.models
import django.contrib.postgres.fields.ranges
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, help_text='The unique ID (UUID4) of this object.', primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, help_text='The date and time when this object was first created.')),
                ('updated', models.DateTimeField(auto_now=True, help_text='The date and time when this object was last updated.')),
                ('title', models.CharField(help_text='The title of this album. Required.', max_length=255)),
                ('description', models.TextField(blank=True, help_text='The description of this album. Optional. Supports markdown.')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='AlbumGroupObjectPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AlbumMember',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, help_text='The unique ID (UUID4) of this object.', primary_key=True, serialize=False)),
                ('period', django.contrib.postgres.fields.ranges.DateTimeRangeField(default=albums.models.from_now_to_forever, help_text='The time range of this album membership. End time can be blank.')),
            ],
        ),
        migrations.CreateModel(
            name='AlbumUserObjectPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
