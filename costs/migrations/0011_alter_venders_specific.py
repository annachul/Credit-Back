# Generated by Django 3.2.8 on 2023-04-14 16:29

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('costs', '0010_alter_venders_specific'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venders',
            name='specific',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), default=list, size=None),
        ),
    ]
