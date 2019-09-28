from django.contrib.gis.db import models

class LocationKind(models.Model):
    name = models.CharField(primary_key=True, max_length=100)

class Location(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=100, null=True)
    coordinates = models.PointField(null=True)
    kinds = models.ManyToManyField(LocationKind)