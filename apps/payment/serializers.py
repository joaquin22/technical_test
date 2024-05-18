from rest_framework import serializers
from .models import Payment, PaymentDetail


class PaymentDetailSerializer(serializers.ModelSerializer):
    loan_external_id = serializers.CharField(read_only=True, source="loan.external_id")

    class Meta:
        model = PaymentDetail
        fields = ["loan_external_id", "amount"]


class PaymentSerializer(serializers.ModelSerializer):

    loans = PaymentDetailSerializer(many=True, read_only=True, source="details")
    customer_external_id = serializers.CharField(write_only=True)
    payment_amount = serializers.CharField(write_only=True)
    total_amount = serializers.FloatField(read_only=True)
    status = serializers.IntegerField(read_only=True)

    class Meta:
        model = Payment
        fields = [
            "external_id",
            "total_amount",
            "customer_external_id",
            "payment_amount",
            "status",
            "paid_at",
            "loans",
        ]
