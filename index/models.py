from django.db import models


class TransportPermit(models.Model):
    names = models.CharField(max_length=255)
