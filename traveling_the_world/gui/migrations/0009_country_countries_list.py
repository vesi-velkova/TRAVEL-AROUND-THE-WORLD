# Generated by Django 5.0.2 on 2024-02-15 23:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gui', '0008_countrylist'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='countries_list',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='gui.countrylist'),
            preserve_default=False,
        ),
    ]
