# Generated by Django 5.0.6 on 2024-06-08 16:04

import users.sentinel
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('files', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='basefile',
            name='uploader',
            field=models.ForeignKey(help_text='The uploader of this file.', on_delete=models.SET(users.sentinel.get_sentinel_user), related_name='files', to=settings.AUTH_USER_MODEL),
        ),
    ]
