from django.db import models


class Play(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()