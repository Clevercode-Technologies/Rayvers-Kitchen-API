# Generated by Django 5.0.1 on 2024-02-02 02:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0004_driver_vehicle_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dish",
            name="restaurant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="dishes",
                to="app.restaurant",
            ),
        ),
    ]