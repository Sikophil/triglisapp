# Generated by Django 4.2.9 on 2024-02-28 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="phone",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
