# Generated by Django 3.2.8 on 2023-04-15 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('costs', '0011_alter_venders_specific'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='name',
            field=models.CharField(max_length=700),
        ),
    ]
