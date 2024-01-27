# Generated by Django 5.0.1 on 2024-01-26 15:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CartItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.PositiveIntegerField()),
            ],
            options={
                "verbose_name": "Cart Item",
                "verbose_name_plural": "Cart Items",
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="DeliveryStatus",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "Pending"),
                            ("OUT_FOR_DELIVERY", "Out for Delivery"),
                            ("DELIVERED", "Delivered"),
                        ],
                        default="PENDING",
                        max_length=20,
                    ),
                ),
            ],
            options={
                "verbose_name": "Delivery Status",
                "verbose_name_plural": "Delivery Status",
            },
        ),
        migrations.CreateModel(
            name="Driver",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "driver_id",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Driver id"
                    ),
                ),
                ("vehicle_color", models.CharField(max_length=40)),
                ("vehicle_description", models.TextField(blank=True)),
                ("vehicle_number", models.CharField(max_length=40)),
                ("available", models.BooleanField(default=False)),
                (
                    "current_location_latitude",
                    models.DecimalField(
                        blank=True, decimal_places=6, max_digits=9, null=True
                    ),
                ),
                (
                    "current_location_longitude",
                    models.DecimalField(
                        blank=True, decimal_places=6, max_digits=9, null=True
                    ),
                ),
            ],
            options={
                "verbose_name": "Driver",
                "verbose_name_plural": "Drivers",
            },
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "file",
                    models.ImageField(upload_to="dishes/", verbose_name="dish image"),
                ),
                ("label", models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("total_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_delivered", models.BooleanField(default=False)),
                ("tracking_url", models.URLField(blank=True, null=True)),
                ("payment_status", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "Order",
                "verbose_name_plural": "Orders",
            },
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.PositiveIntegerField()),
            ],
            options={
                "verbose_name": "Order Item",
                "verbose_name_plural": "Order Items",
            },
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("payment_method", models.CharField(max_length=50)),
                ("transaction_id", models.CharField(max_length=100)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("payment_date", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Payment",
                "verbose_name_plural": "Payments",
            },
        ),
        migrations.CreateModel(
            name="PersonalMessage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Personal Message",
                "verbose_name_plural": "Personal Messages",
            },
        ),
        migrations.CreateModel(
            name="Restaurant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "kitchen_id",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Kitchen id"
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("ratings", models.IntegerField(default=0)),
            ],
            options={
                "verbose_name": "Restaurant",
                "verbose_name_plural": "Restaurants",
            },
        ),
        migrations.CreateModel(
            name="ShoppingCart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "verbose_name": "Cart",
                "verbose_name_plural": "Shopping Cart",
            },
        ),
        migrations.CreateModel(
            name="Dish",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
                ("description", models.TextField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("ratings", models.IntegerField(default=0)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dish_category",
                        to="app.category",
                    ),
                ),
            ],
            options={
                "verbose_name": "Dish",
                "verbose_name_plural": "Dishes",
            },
        ),
    ]
