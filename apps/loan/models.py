from django.db import models
from utils.mixins import TimestampMixin
from apps.customer.models import Customer


class Loan(TimestampMixin, models.Model):

    class Status(models.IntegerChoices):
        PENDING = 1
        ACTIVE = 2
        REJECTED = 3
        PAID = 4

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    external_id = models.CharField("External ID", max_length=60, unique=True)
    amount = models.FloatField("Amount")
    outstanding = models.FloatField("Outstanding")
    contract_version = models.CharField(
        "Contract Version", max_length=30, blank=True, null=True, default=""
    )
    status = models.PositiveSmallIntegerField(
        "Status", choices=Status.choices, default=Status.PENDING
    )
    taken_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Loan"
        verbose_name_plural = "Loans"

    def __str__(self):
        return f"{self.external_id} - {self.outstanding} - {self.status}"
