from django.db import models

from apps.user_profile.models import Operator
from apps.antecipation.models import RequestAntecipation


class Antecipation(models.Model):
    requester = models.OneToOneField(Operator, on_delete=models.SET_NULL, null=True, related_name='operator')
    payment = models.OneToOneField(RequestAntecipation, on_delete=models.SET_NULL, null=True, related_name='request')
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.payment} - {self.fee}'
