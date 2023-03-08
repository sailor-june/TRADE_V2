# Generated by Django 4.1.5 on 2023-03-05 22:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("main_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="inventory",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
