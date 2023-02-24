from rest_framework import serializers

from apps.payment.models import Payment
from apps.antecipation.models import RequestAntecipation, Antecipation


class AntecipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Antecipation
        fields = '__all__'


class RequestAntecipationSerializer(serializers.ModelSerializer):
    request = AntecipationSerializer(read_only=True)

    class Meta:
        model = RequestAntecipation
        fields = [
            'payment',
            'requester',
            'request_date',
            'fee',
            'status',
            'created',
            'updated',
            'request'
        ]


class PaymentSerializer(serializers.ModelSerializer):
    anticipation = RequestAntecipationSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = [
            'supplier',
            'description',
            'value',
            'date_due',
            'is_active',
            'created',
            'anticipation',
        ]
