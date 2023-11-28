from django.db import models


# Create your models here.

class Passwords(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)


class nonCSVPasswords(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
