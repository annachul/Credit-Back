# Generated by Django 3.2.8 on 2023-03-21 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('costs', '0006_alter_payment_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=models.DateField(),
        ),
    ]
