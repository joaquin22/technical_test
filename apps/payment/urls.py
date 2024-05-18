from django.urls import path, include
from rest_framework import routers

from .views import PaymentView

app_name = "payment"


router = routers.DefaultRouter()
router.register(r"payment", PaymentView, basename="payment")

urlpatterns = [path("", include(router.urls))]

# urlpatterns = [
#     path("payment/", PaymentView.as_view(), name="payment"),
#     # path("payment/<slug:customer_id>/", PaymentView.as_view(), name="payment"),
# ]
