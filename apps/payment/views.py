from django.db.models import Sum

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


from apps.customer.models import Customer
from apps.loan.models import Loan

from .models import Payment, PaymentDetail
from .serializers import PaymentSerializer


class PaymentView(GenericAPIView):

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):

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
        if payment_amount <= total_outstanding["total"]:

            payment = Payment.objects.create(
                customer=customer,
                total_amount=payment_amount,
                **request.data,
            )

            payment_amount_tmp = payment_amount  # 100

            for loan in loans:

                if payment_amount_tmp == 0:
                    break

                loan_payment = 0

                result = payment_amount_tmp - loan.outstanding
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
            return Response("Insufficient funds", status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        customer_id = kwargs.get("customer_id")
        customer = Customer.objects.get(pk=customer_id)
        payments = Payment.objects.filter(customer=customer).all()
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)


# POST
# {external_id, customer_external_id, loan_external_id,payment_amount}

# GET
# [
#     {external_id, customer_external_id, loan_external_id,payment_amount,date,status,total_amount}
# ]
