from rest_framework import serializers

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):

    preapproved_at = serializers.DateTimeField(read_only=True)
    status = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ["external_id", "status", "score", "preapproved_at"]
