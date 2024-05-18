import datetime

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from apps.customer.models import Customer

from .models import Loan
from .serializers import LoanSerializer


class LoanViewSet(viewsets.ModelViewSet):
    """
    list: Return a list of loans
    create: Create a new loan
    read: Return a single loan use the {external_id} as parameter
    loan_by_customer: Return a list of loans by customer use the {customer_external_id} as parameter
    activate: Activate a loan use the {external_id} as parameter
    reject: Reject a loan use the {external_id} as parameter
    """

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [HasAPIKey]
    http_method_names = ["get", "post"]
    lookup_field = "external_id"

    @action(detail=True, methods=["post"])
    def activate(self, request, external_id=None):
        loan = Loan.objects.get(external_id=external_id)

        if loan.status == Loan.Status.PENDING:
            loan.status = Loan.Status.ACTIVE
            loan.taken_at = datetime.datetime.now()
            loan.save()

        serializer = self.get_serializer(loan)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def reject(self, request, external_id=None):
        loan = Loan.objects.get(external_id=external_id)

        if loan.status == Loan.Status.PENDING:
            loan.status = Loan.Status.REJECTED
            loan.save()

        serializer = self.get_serializer(loan)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def loan_by_customer(self, request, external_id=None):
        customer = Customer.objects.get(external_id=external_id)

        loans = Loan.objects.filter(customer=customer).all()

        serializer = self.get_serializer(loans, many=True)
        return Response(serializer.data)
