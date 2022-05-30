# Generated by Django 3.2.12 on 2022-05-30 05:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('galleries', '0001_initial'),
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='gallery',
            field=models.ForeignKey(help_text='The gallery this file belongs to.', on_delete=django.db.models.deletion.CASCADE, related_name='gallery_documents', to='galleries.gallery'),
        ),
    ]
