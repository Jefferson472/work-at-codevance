from django.test import TestCase

from apps.core.models import CustomUser
from apps.user_profile.models import Supplier


class TestSupplierModel(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email='supplier@test.com')
        self.suplier = Supplier.objects.create(user=self.user, cnpj='12345678901234', name='Suplier Test')

    def test_cnpj_max_length(self):
        max_length = self.suplier._meta.get_field('cnpj').max_length
        self.assertEquals(max_length, 14)

    def test_str_method(self):
        self.assertEquals(str(self.suplier), 'Suplier Test')


class TestOperatorModel(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email='operator@test.com')
        self.operator = Supplier.objects.create(user=self.user, name='Operator Test')

    def test_str_method(self):
        self.assertEquals(str(self.operator), 'Operator Test')
