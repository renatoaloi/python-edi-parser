from django.db import models


class UniqueWithin30daysEntity(models.Model):
    field = models.IntegerField()
    date_created = models.DateField(auto_now_add=True)


class UniqueEntity(models.Model):
    field = models.IntegerField()


class DistinctEntity(models.Model):
    field = models.IntegerField()