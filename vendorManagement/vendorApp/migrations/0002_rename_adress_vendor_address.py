# Generated by Django 5.0 on 2023-12-22 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendorApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vendor',
            old_name='adress',
            new_name='address',
        ),
    ]
