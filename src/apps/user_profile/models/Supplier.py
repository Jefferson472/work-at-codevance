from django.db import models

from apps.user_profile.models import BaseProfile


class Supplier(BaseProfile):
    cnpj = models.CharField(max_length=14, verbose_name='CNPJ')

    class Meta:
        verbose_name = "Suplier Profile"
