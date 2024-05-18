from django.urls import path, include
from rest_framework import routers

from .views import CustomerViewSet

app_name = "customer"


router = routers.DefaultRouter()
router.register(r"customer", CustomerViewSet, basename="customer")

urlpatterns = [path("", include(router.urls))]
