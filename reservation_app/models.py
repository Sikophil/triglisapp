# models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    time = models.TimeField(default='12:00:00')
    date = models.DateField(default='2024-02-19')

    def __str__(self):
        return f"{self.user.username} - {self.user.last_name} - {self.date} - {self.time}"

