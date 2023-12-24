# Generated by Django 5.0 on 2023-12-22 17:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendorApp', '0002_rename_adress_vendor_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalperfomance',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historical_perfomances', to='vendorApp.vendor'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_orders', to='vendorApp.vendor'),
        ),
    ]