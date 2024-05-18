from django.urls import path, include
from rest_framework import routers

from .views import LoanViewSet

app_name = "loan"


router = routers.DefaultRouter()
router.register(r"loan", LoanViewSet, basename="loan")

urlpatterns = [path("", include(router.urls))]
