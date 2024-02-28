# models.py
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class Book(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    time = models.TimeField(default='12:30:00')
    date = models.DateField(default='2024-02-19')
    guests = models.IntegerField(default= '',null=False)
    confirmation= models.CharField(default='Nein', max_length=20)

    def __str__(self):
        return f"{self.user.username} - {self.user.last_name} - {self.date} - {self.time} - {self.guests} - {self.confirmation}"

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
