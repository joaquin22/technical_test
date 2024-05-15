from django.db import models
import datetime

class TimestampMixin(models.Model):
    created_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField(default=datetime.datetime.now)
    class Meta:
        abstract = True