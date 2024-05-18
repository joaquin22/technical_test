import datetime
from django.db import models


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        abstract = True
