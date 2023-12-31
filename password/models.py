from django.db import models


# Create your models here.

class Passwords(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)


class NonCSV(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

