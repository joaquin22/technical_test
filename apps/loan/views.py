import datetime

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.customer.models import Customer

from .models import Loan
from .serializers import LoanSerializer


class LoanViewSet(viewsets.ModelViewSet):

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        loan = Loan.objects.get(external_id=pk)

        if loan.status == Loan.Status.PENDING:
            loan.status = Loan.Status.ACTIVE
            loan.taken_at = datetime.datetime.now()
            loan.save()

        serializer = self.get_serializer(loan)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        loan = Loan.objects.get(external_id=pk)

        if loan.status == Loan.Status.PENDING:
            loan.status = Loan.Status.REJECTED
            loan.save()

        serializer = self.get_serializer(loan)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def loan_by_customer(self, request, pk=None):
        customer = Customer.objects.get(external_id=pk)

        loans = Loan.objects.filter(customer=customer).all()

        serializer = self.get_serializer(loans, many=True)
        return Response(serializer.data)
