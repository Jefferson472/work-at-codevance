from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from apps.antecipation.models import RequestAntecipation
from apps.core.models import CustomUser
from apps.payment.models import Payment
from apps.user_profile.models import Supplier


class PaymentListViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(email='user@test.com')
        self.supplier = Supplier.objects.create(user=self.user, name='Test Supplier')
        self.payment1 = Payment.objects.create(supplier=self.supplier, value=100.0, date_due='2023-02-28', is_active=True)
        self.payment2 = Payment.objects.create(supplier=self.supplier, value=200.0, date_due='2023-02-28', is_active=True)
        self.payment3 = Payment.objects.create(supplier=self.supplier, value=300.0, date_due='2023-02-28', is_active=False)

    def test_payment_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('api_payment_list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_payment_list_view_filter_status(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('api_payment_list_status', kwargs={'status': 'avaliable'}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['id'], self.payment1.id)
        self.assertEqual(response.data[1]['id'], self.payment2.id)


class RequestAntecipationCreateAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email='user@test.com')
        self.supplier = Supplier.objects.create(user=self.user, name='Test Supplier')
        self.payment = Payment.objects.create(supplier=self.supplier, value=100.0, date_due='2023-02-28', is_active=True)

    def test_create_request_antecipation_success(self):
        url = reverse('request_antecipation_create')
        data = {
            'payment': self.payment.id,
            'request_date': '2022-12-01'
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, 'Antecipation request successfully sended!')
        self.assertEqual(RequestAntecipation.objects.count(), 1)

    def test_create_request_antecipation_payment_not_found(self):
        url = reverse('request_antecipation_create')
        data = {
            'payment': 9999,
            'request_date': '2022-12-01'
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {'detail': 'The requested payment was not found in the payment list'})
        self.assertEqual(RequestAntecipation.objects.count(), 0)
