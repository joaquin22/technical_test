from django.contrib import admin

from .models import Payment, PaymentDetail

admin.site.register(Payment)
admin.site.register(PaymentDetail)
