from django.db import models

# Create your models here.
class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    weight = models.IntegerField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name