# Generated by Django 5.0.3 on 2024-04-05 23:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0005_alter_dish_images"),
    ]

    operations = [
        migrations.AlterField(
            model_name="driver",
            name="vehicle_image",
            field=models.ImageField(
                blank=True, null=True, upload_to="driver/", verbose_name="vehicle image"
            ),
        ),
    ]
