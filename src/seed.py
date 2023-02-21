# encoding: utf-8

from apps.core.models import CustomUser
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


# creating suplier profile
user_supplier = CustomUser.objects.create(
    email="supplier@test.com",
)

user_operator.set_password("test123456")
user_operator.save()

supplier = Supplier.objects.create(
    user=user_supplier,
    name="Supplier",
)
