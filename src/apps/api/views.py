from rest_framework.generics import ListAPIView

from apps.api.serializers import PaymentSerializer
from apps.payment.models import Payment


class PaymentListView(ListAPIView):
    queryset = Payment.objects.select_related('req_antecipation')
    serializer_class = PaymentSerializer
