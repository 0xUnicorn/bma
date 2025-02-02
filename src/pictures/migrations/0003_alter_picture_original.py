# Generated by Django 4.1.1 on 2022-09-24 20:14

from django.db import migrations, models
import pictures.models


class Migration(migrations.Migration):

    dependencies = [
        ("pictures", "0002_picture_tags"),
    ]

    operations = [
        migrations.AlterField(
            model_name="picture",
            name="original",
            field=models.ImageField(
                help_text="The original uploaded picture file.",
                max_length=255,
                upload_to=pictures.models.get_picture_upload_path,
            ),
        ),
    ]
