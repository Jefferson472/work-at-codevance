from rest_framework.generics import ListAPIView

from apps.api.serializers import PaymentSerializer
from apps.payment.models import Payment


class PaymentListView(ListAPIView):
    queryset = Payment.objects.select_related('anticipation')
    serializer_class = PaymentSerializer
