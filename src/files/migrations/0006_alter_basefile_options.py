# Generated by Django 5.0.3 on 2024-04-14 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0005_alter_basefile_options_alter_basefile_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='basefile',
            options={'ordering': ('created',), 'permissions': (('unapprove_basefile', 'Unapprove file'), ('approve_basefile', 'Approve file'), ('unpublish_basefile', 'Unpublish file'), ('publish_basefile', 'Publish file')), 'verbose_name': 'file', 'verbose_name_plural': 'files'},
        ),
    ]
