# Generated by Django 5.0.6 on 2024-08-24 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="EmailSubscription",
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
                ("email", models.EmailField(max_length=254, unique=True)),
                ("is_confirmed", models.BooleanField(default=False)),
                ("confirmation_code", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="WeatherHistory",
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
                ("city", models.CharField(max_length=100)),
                ("description", models.CharField(max_length=255)),
                ("temperature", models.FloatField()),
                ("wind_speed", models.FloatField()),
                ("humidity", models.IntegerField()),
                ("date", models.DateField(auto_now_add=True)),
            ],
        ),
    ]
