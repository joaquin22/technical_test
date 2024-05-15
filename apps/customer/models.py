import datetime

from django.db import models
from utils.mixins import  TimestampMixin


# Create your models here.

class Customer(TimestampMixin,models.Model):

    class Status(models.IntegerChoices):
        ACTIVE = 1
        INACTIVE = 2

    external_id = models.CharField("External ID", max_length=60)
    score = models.FloatField("Score",default=1000)
    status = models.PositiveSmallIntegerField("Status",choices=Status)
    preapproved_at = models.DateTimeField(default=datetime.datetime.now)


    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return f"{self.external_id} - {self.status}"