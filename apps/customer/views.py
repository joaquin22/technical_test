from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from django.db.models import Sum, Q

from apps.loan.models import Loan

from .models import Customer
from .serializers import CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    """
    list: Return a list of customers
    retrieve: Return a single customer use the {external_id} as parameter
    create: Create a new customer
    balance: Return the balance of a customer use the {external_id} as parameter
    """

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [HasAPIKey]
    http_method_names = ["get", "post"]
    lookup_field = "external_id"

    def retrieve(self, request, *args, **kwargs):
        customer = Customer.objects.get(external_id=kwargs["external_id"])
        serializer = self.get_serializer(customer)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def balance(self, request, external_id=None):
        customer = Customer.objects.get(external_id=external_id)
        outstanding_sum = Loan.objects.filter(
            Q(status=Loan.Status.ACTIVE) | Q(status=Loan.Status.PENDING),
            customer=customer,
        ).aggregate(total_debt=Sum("outstanding"))

        if outstanding_sum["total_debt"] is None:
            outstanding_sum["total_debt"] = 0

        response_data = {
            "external_id": customer.external_id,
            "score": customer.score,
            "total_debt": outstanding_sum["total_debt"],
            "available_amount": (customer.score - outstanding_sum["total_debt"]),
        }

        return Response(response_data)
