# models.py
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class Book(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    last_name = models.CharField(default='', max_length=50)
    time = models.TimeField(default='12:30:00')
    date = models.DateField(default='2024-02-19')
    guests = models.IntegerField(default= '',null=False)
    confirmation= models.CharField(default='Nein', max_length=20)
    fcm_token = models.CharField(max_length=255, blank=True, null=True)
    phone     = models.CharField(max_length=30,blank=True,null=True)

    def __str__(self):
        if self.name == '': 
            return f" - {self.date} - {self.time} - {self.guests} - {self.confirmation}"
        else:
            return f"{self.last_name} - {self.date} - {self.time} - {self.guests} - {self.confirmation}"

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
