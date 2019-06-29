from django.db import models


class UniqueWithin30daysEntity(models.Model):
    field = models.IntegerField()
    date_created = models.DateField(auto_now_add=True)


class UniqueEntity(models.Model):
    field = models.IntegerField()


class DistinctEntity(models.Model):
    field = models.IntegerField()


class SaveFieldEntity(models.Model):
    field = models.IntegerField()
    position = models.IntegerField()
    registro = models.CharField(max_length=200, default='')


class SumFieldEntity(models.Model):
    field = models.IntegerField()
    position = models.IntegerField()
    registro = models.CharField(max_length=200)
