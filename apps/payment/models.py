import datetime

from django.db import models
from utils.mixins import TimestampMixin

from apps.customer.models import Customer
from apps.loan.models import Loan


class Payment(TimestampMixin, models.Model):

    class Status(models.IntegerChoices):
        COMPLETED = 1
        REJECTED = 2

    external_id = models.CharField("External ID", max_length=60, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(
        "Status", choices=Status.choices, default=Status.COMPLETED
    )
    total_amount = models.FloatField()
    paid_at = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return f"{self.external_id}"


class PaymentDetail(TimestampMixin, models.Model):

    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, related_name="details"
    )
    amount = models.FloatField()

    class Meta:
        verbose_name = "PaymetDetail"
        verbose_name_plural = "PaymetDetails"

    def __str__(self):
        return f"{self.payment} - {self.amount}"
