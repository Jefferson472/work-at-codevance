from rest_framework.generics import ListAPIView

from apps.api.serializers import PaymentSerializer
from apps.payment.models import Payment


class PaymentListView(ListAPIView):
    queryset = Payment.objects.all().select_related('req_antecipation')
    serializer_class = PaymentSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        if not self.request.user.has_perm('user_profile.payment_view'):
            qs = qs.filter(supplier__user=self.request.user)

        query = self.kwargs.get('status')
        if query:
            status = {
                'unavailable': qs.filter(is_active=False),
                'avaliable': qs.filter(is_active=True, req_antecipation=None),
                'requested': qs.exclude(req_antecipation=None),
                'approval': qs.filter(req_antecipation__status='1'),
                'disapproval': qs.filter(req_antecipation__status='2'),
            }
            return status[query]
        return qs
