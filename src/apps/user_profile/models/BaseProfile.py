from django.db import models

from apps.core.models import CustomUser


class BaseProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=55)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
