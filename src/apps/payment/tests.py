from django.test import TestCase

from apps.payment.models import Payment
from apps.user_profile.models import Supplier


class PaymentModelTestCase(TestCase):
    def setUp(self):
        self.supplier = Supplier.objects.create(name='Test Supplier')
        self.payment = Payment.objects.create(
            supplier=self.supplier,
            description='Test Payment',
            value=100.00,
            date_due='2023-12-31',
        )

    def test_payment_creation(self):
        self.assertEqual(Payment.objects.count(), 1)

    def test_payment_defaults(self):
        self.assertTrue(self.payment.is_active)
        self.assertIsNotNone(self.payment.created)
