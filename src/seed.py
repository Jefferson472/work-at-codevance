# encoding: utf-8

import random

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from apps.core.models import CustomUser
from apps.payment.models import Payment
from apps.user_profile.models import Operator, Supplier


# creating SuperUser
super_user = CustomUser.objects.create_superuser(
    email="admin@test.com", password="test123456"
)


# creating operator profile
user_operator = CustomUser.objects.create(
    email="operator@test.com",
)

user_operator.set_password("test123456")
user_operator.save()

operator = Operator.objects.create(
    user=user_operator,
    name="Operator",
)

content_type = ContentType.objects.get_for_model(Operator)
all_permissions = Permission.objects.filter(content_type=content_type)
operator.user.user_permissions.set(all_permissions)


# creating suplier profile
user_supplier = CustomUser.objects.create(
    email="supplier@test.com",
)

user_supplier.set_password("test123456")
user_supplier.save()

supplier = Supplier.objects.create(
    user=user_supplier,
    name="Supplier",
)


# creating payments
PAYMENTS_INFO = [
    {'description': 'Pagamento Teste 1', 'date_due': '2023-01-01'},
    {'description': 'Pagamento Teste 2', 'date_due': '2023-02-01'},
    {'description': 'Pagamento Teste 3', 'date_due': '2023-03-01'},
    {'description': 'Pagamento Teste 4', 'date_due': '2023-04-01'},
    {'description': 'Pagamento Teste 5', 'date_due': '2023-05-01'},
]
payments = []
for payment in PAYMENTS_INFO:
    payments.append(Payment(
        supplier=supplier,
        description=payment['description'],
        value=random.randrange(100, 1000),
        date_due=payment['date_due'],
    ))

Payment.objects.bulk_create(payments)
