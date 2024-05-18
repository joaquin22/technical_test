from django.db.models import Sum

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_api_key.permissions import HasAPIKey


from apps.customer.models import Customer
from apps.loan.models import Loan

from .models import Payment, PaymentDetail
from .serializers import PaymentSerializer


class PaymentView(viewsets.GenericViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [HasAPIKey]

    def create(self, request, *args, **kwargs):

        customer_id = request.data.pop("customer_external_id")
        payment_amount = request.data.pop("payment_amount")

        customer = Customer.objects.get(external_id=customer_id)
        loans = Loan.objects.filter(
            status=Loan.Status.ACTIVE,
            customer=customer,
        ).all()

        if not loans.exists():
            return Response("No active loans", status=status.HTTP_400_BAD_REQUEST)

        total_outstanding = loans.aggregate(total=Sum("outstanding"))
        print(total_outstanding)
        if payment_amount <= total_outstanding["total"]:

            payment = Payment.objects.create(
                customer=customer,
                total_amount=payment_amount,
                **request.data,
            )

            payment_amount_tmp = payment_amount

            for loan in loans:

                if payment_amount_tmp == 0:
                    break

                loan_payment = 0

                result = payment_amount_tmp - loan.outstanding  # 700 - 500 = 200

                if result >= 0:
                    payment_amount_tmp = result
                    loan_payment = loan.outstanding
                else:
                    loan_payment = payment_amount_tmp
                    payment_amount_tmp = 0

                PaymentDetail.objects.create(
                    payment=payment,
                    loan=loan,
                    amount=loan_payment,
                )

                new_outstanding = loan.outstanding - loan_payment
                if new_outstanding == 0:
                    loan.status = Loan.Status.PAID

                loan.outstanding = new_outstanding
                loan.save()

            serializer = self.get_serializer(payment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(
                "Payment_amount is greater than total outstanding",
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["get"])
    def payment_by_customer(self, request, pk=None):
        customer = Customer.objects.get(external_id=pk)
        payments = Payment.objects.filter(customer=customer).all()
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def reject_payment(self, request, pk=None):
        payment = Payment.objects.get(external_id=pk)
        payment.status = Payment.Status.REJECTED
        payment_detail = payment.details.all()

        loans_ids = payment_detail.values_list("loan__external_id", flat=True)
        loans = Loan.objects.filter(external_id__in=loans_ids).all()

        for loan in loans:
            loan.status = Loan.Status.ACTIVE
            amount = payment_detail.get(loan=loan).amount
            loan.outstanding = amount
            loan.save()

        payment.save()
        return Response("OK")
