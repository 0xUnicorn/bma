# Generated by Django 3.2.12 on 2022-05-30 05:13

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('photos', '0001_initial'),
        ('utils', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='The tags for this photo', through='utils.UUIDTaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
