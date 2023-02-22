from django.test import TestCase
from django.urls import resolve, reverse

from apps.core.models import CustomUser
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


class TestUrls(TestCase):
    def test_payments_url(self):
        self.assertEqual(reverse('payments_list'), '/payments/')
        self.assertEqual(resolve('/payments/').view_name, 'payments_list')


class TestPaymentListView(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email='user@test.com')

    def test_payment_list_view_anonymous_302(self):
        response = self.client.get('/payments/')
        self.assertEqual(response.status_code, 302)

    def test_payment_list_view_authenticated_200(self):
        self.client.force_login(self.user)
        response = self.client.get('/payments/')
        self.assertEqual(response.status_code, 200)
