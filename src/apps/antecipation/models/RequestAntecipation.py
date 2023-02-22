from datetime import date
from decimal import Decimal
from django.db import models


from apps.core.models import CustomUser
from apps.payment.models import Payment


TAX = 3 / 100
DAILY_TAX = Decimal(TAX / 30)


class RequestAntecipation(models.Model):
    STATUS_CHOICES = (
        ('0', 'Aguardando avaliação'),
        ('1', 'Aprovado'),
        ('2', 'Não aprovado'),
    )

    payment = models.OneToOneField(Payment, on_delete=models.SET_NULL, null=True, related_name='anticipation')
    requester = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='requester')
    request_date = models.DateField()
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.payment} - {self.get_status_display()}'

    @property
    def calculated_fee(self):
        if self.payment.date_due > date.today():
            difference = self.payment.date_due - self.request_date
            fee = self.payment.value * DAILY_TAX * difference.days
            return fee
        return 0
