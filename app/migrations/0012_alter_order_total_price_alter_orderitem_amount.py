# Generated by Django 5.0.1 on 2024-02-08 08:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0011_alter_dish_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="total_price",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="amount",
            field=models.IntegerField(),
        ),
    ]