from django.db import models

from apps.user_profile.models import Operator
from apps.antecipation.models import RequestAntecipation


class LogTransactions(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.SET_NULL, null=True)
    request_antecipation = models.OneToOneField(RequestAntecipation, on_delete=models.SET_NULL, null=True)
    status_after = models.CharField(max_length=20)
    value_before = models.DecimalField(max_digits=10, decimal_places=2)
    value_after = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
