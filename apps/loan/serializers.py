from rest_framework import serializers

from .models import Loan, Customer


class LoanSerializer(serializers.ModelSerializer):
    customer_external_id = serializers.CharField(write_only=True)
    status = serializers.IntegerField(read_only=True)

    class Meta:
        model = Loan
        fields = [
            "external_id",
            "customer_external_id",
            "amount",
            "outstanding",
            "status",
        ]

    def create(self, validated_data):
        customer_external_id = validated_data.pop("customer_external_id")
        customer = Customer.objects.get(external_id=customer_external_id)
        obj = Loan.objects.create(**validated_data, customer=customer)
        return obj

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["customer_external_id"] = instance.customer.external_id
        return ret
