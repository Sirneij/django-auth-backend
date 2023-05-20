# Generated by Django 4.2.1 on 2023-05-16 17:55

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "01_added_user_and_profile_model"),
    ]

    operations = [
        migrations.CreateModel(
            name="Series",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=20000)),
                ("image", models.ImageField(upload_to="series/")),
            ],
            options={
                "verbose_name_plural": "Series",
            },
        ),
        migrations.CreateModel(
            name="Articles",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(max_length=20000)),
                ("url", models.URLField()),
                (
                    "series",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.series"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Articles",
            },
        ),
    ]
