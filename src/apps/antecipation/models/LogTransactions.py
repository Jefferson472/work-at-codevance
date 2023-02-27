from django.db import models

from apps.core.models import CustomUser
from apps.antecipation.models import RequestAntecipation


class LogTransactions(models.Model):
    TRANSACTION_TYPE = (
        ('0', 'Request'),
        ('1', 'Approval'),
        ('2', 'Disapproval'),
    )

    requester = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    req_antecipation = models.ForeignKey(RequestAntecipation, on_delete=models.SET_NULL, null=True)
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPE)
    status_after = models.CharField(max_length=20)
    value_before = models.DecimalField(max_digits=10, decimal_places=2)
    value_after = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
