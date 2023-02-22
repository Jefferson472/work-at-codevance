from celery import shared_task
from django.utils import timezone

from apps.payment.models import Payment


@shared_task
def check_payment_due_date():
    payments = Payment.objects.filter(is_active=True)
    for payment in payments:
        if timezone.now().date() > payment.date_due:
            payment.is_active = False
    Payment.objects.bulk_update(payments, ['is_active'])
