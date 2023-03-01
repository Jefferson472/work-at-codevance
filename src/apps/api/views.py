from datetime import datetime

from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.serializers import PaymentSerializer, RequestAntecipationCreateSerializer
from apps.antecipation.models import DAILY_TAX
from apps.antecipation.tasks import log_create, send_email
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
            if query in status:
                return status[query]
            else:
                raise NotFound(detail="The requested status was not found in the payment list", code=404)
        return qs


class RequestAntecipationCreateAPIView(APIView):
    def post(self, request):
        data = request.data
        serializer = RequestAntecipationCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        payment = Payment.objects.filter(id=data.get('payment'), supplier__user=request.user).first()
        if not payment or not payment.is_active:
            return Response({'detail': 'Pagamento não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        difference = payment.date_due - datetime.strptime(data.get('request_date'), '%Y-%m-%d').date()
        fee = payment.value * DAILY_TAX * difference.days

        serializer.save(payment=payment, requester=request.user, fee=fee, request_date=data.get('request_date'))

        log_create.delay(serializer.instance.id, request.user.id, type='0')
        msg = 'Pedido de antecipação encaminhado com sucesso!'
        send_email.delay(payment.id, msg)

        return Response(msg, status=status.HTTP_201_CREATED)
