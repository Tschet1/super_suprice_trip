from django.contrib.gis.db import models
from mptt.models import MPTTModel, TreeForeignKey

class EventCategory(MPTTModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

class Event(models.Model):
    id = models.IntegerField(primary_key=True)
    event_name = models.CharField(max_length=100, null=True)
    venue_name = models.CharField(max_length=100, null=True)
    date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    coordinates = models.PointField(null=True)
    categories = models.ManyToManyField(EventCategory)
    nearest_public_transport = models.CharField(max_length=100)