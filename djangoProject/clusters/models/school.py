from django.db import models


class School(models.Model):
    name = models.TextField()
    type = models.CharField(max_length=200)
    cite = models.CharField(max_length=100)
