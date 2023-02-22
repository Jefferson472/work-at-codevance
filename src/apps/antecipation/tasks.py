from django.conf import settings
from django.core.mail import send_mail

from apps.antecipation.models import LogTransactions, RequestAntecipation
from apps.core.models import CustomUser
from apps.payment.models import Payment


def log_create(req_antecipation_id, user_id, type):
    req_antecipation = RequestAntecipation.objects.get(id=req_antecipation_id)
    requester = CustomUser.objects.get(id=user_id)
    LogTransactions.objects.create(
        requester=requester,
        request_antecipation=req_antecipation,
        transaction_type=type,
        status_after=req_antecipation.get_status_display(),
        value_before=req_antecipation.payment.value,
        value_after=req_antecipation.payment.value - req_antecipation.fee,
    )


def send_email(payment_id, msg):
    payment = Payment.objects.get(id=payment_id)
    subject = f'Status do Pagamento {payment.id} alterado'

    return send_mail(
        subject, msg, settings.DEFAULT_FROM_EMAIL, [payment.supplier.user.email]
    )
