from rest_framework import serializers

from apps.payment.models import Payment
from apps.antecipation.models import RequestAntecipation, Antecipation


class AntecipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Antecipation
        fields = '__all__'


class RequestAntecipationSerializer(serializers.ModelSerializer):
    antecipation = AntecipationSerializer(read_only=True)

    class Meta:
        model = RequestAntecipation
        fields = [
            'id',
            'payment',
            'requester',
            'request_date',
            'fee',
            'status',
            'created',
            'updated',
            'antecipation'
        ]


class RequestAntecipationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestAntecipation
        fields = [
            'payment',
            'requester',
            'request_date',
        ]

    def get_fee(self, obj):
        return obj.calculated_fee

class PaymentSerializer(serializers.ModelSerializer):
    req_antecipation = RequestAntecipationSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id',
            'supplier',
            'description',
            'value',
            'date_due',
            'is_active',
            'created',
            'req_antecipation',
        ]


class RequestAntecipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestAntecipation
        fields = ['id', 'payment_id', 'requester', 'fee']