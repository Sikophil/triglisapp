# Generated by Django 4.2.9 on 2024-03-05 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reservation_app", "0010_book_color"),
    ]

    operations = [
        migrations.AddField(
            model_name="notification", name="title", field=models.TextField(default=""),
        ),
        migrations.AlterField(
            model_name="notification",
            name="message",
            field=models.TextField(default=""),
        ),
    ]
