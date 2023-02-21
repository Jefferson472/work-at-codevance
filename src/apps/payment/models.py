from django.db import models

from apps.user_profile.models import Supplier


class Payment(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, related_name='supplier')
    description = models.CharField(max_length=255, blank=True, null=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    date_due = models.DateField()
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.supplier} - {self.value} - {self.date_due}'
