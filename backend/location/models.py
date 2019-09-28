from django.contrib.gis.db import models

class Location(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    coordinates = models.PointField()