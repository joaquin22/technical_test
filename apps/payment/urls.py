from django.urls import path, include
from rest_framework import routers

from .views import PaymentView

app_name = "payment"


urlpatterns = [
    path("payment/", PaymentView.as_view(), name="payment"),
    path("payment/<int:customer_id>/", PaymentView.as_view(), name="payment"),
]
