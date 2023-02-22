from apps.user_profile.models import BaseProfile


class Operator(BaseProfile):
    class Meta:
        verbose_name = "Operator Profile"
        permissions = [
            ('payment_view', 'Can see all payments'),
            ('payment_create', 'Can create new payments'),
        ]
