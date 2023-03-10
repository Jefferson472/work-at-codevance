import random
import string
from datetime import date, timedelta

from django.test import TestCase
from django.urls import resolve, reverse

from apps.antecipation.models import Antecipation, LogTransactions, RequestAntecipation
from apps.antecipation.models.RequestAntecipation import DAILY_TAX
from apps.core.models import CustomUser
from apps.payment.models import Payment
from apps.user_profile.models import Operator


class BaseTestCase(TestCase):
    def setUp(self):
        random_email = ''.join(random.choice(string.ascii_letters) for _ in range(10)) + '@test.com'
        self.user_operator = CustomUser.objects.create(email=random_email)
        self.operator = Operator.objects.create(
            user=self.user_operator,
            name='Operator',
        )
        self.payment = Payment.objects.create(
            value=1000,
            date_due='2023-02-20'
        )
        self.request_antecipation = RequestAntecipation.objects.create(
            payment=self.payment,
            requester=self.user_operator,
            request_date='2023-02-01',
            fee=0,
        )


class RequestAntecipationTestCase(BaseTestCase):
    def test_request_antecipation_str(self):
        self.assertEqual(str(self.request_antecipation), f'{self.payment} - Aguardando avaliação')

    def test_request_antecipation_status_choices(self):
        self.assertEqual(self.request_antecipation.get_status_display(), 'Aguardando avaliação')

    def test_calculated_fee(self):
        payment = Payment.objects.create(value=1000, date_due=date.today() + timedelta(days=1))
        expected_fee = payment.value * DAILY_TAX * 1
        request_antecipation = RequestAntecipation.objects.create(
            payment=payment, requester_id=1, request_date=date.today(), fee=expected_fee,
        )
        self.assertEqual(request_antecipation.calculated_fee, expected_fee)


class AntecipationModelTestCase(BaseTestCase):
    def test_antecipation_creation(self):
        Antecipation.objects.create(
            operator=self.operator,
            req_antecipation=self.request_antecipation,
            new_value=5.00
        )
        self.assertEqual(Antecipation.objects.count(), 1)


class LogTransactionsModelTestCase(BaseTestCase):
    def test_log_transactions_creation(self):
        LogTransactions.objects.create(
            requester=self.user_operator,
            req_antecipation=self.request_antecipation,
            status_after="approved",
            value_before=100.0,
            value_after=90.0
        )
        self.assertEqual(LogTransactions.objects.count(), 1)


class TestUrls(TestCase):
    def test_antecipation_url(self):
        self.assertEqual(reverse('antecipations_list'), '/antecipations/')
        self.assertEqual(resolve('/antecipations/').view_name, 'antecipations_list')

    def test_request_antecipation_url(self):
        self.assertEqual(reverse('request_antecipations_list'), '/antecipations-request/')
        self.assertEqual(resolve('/antecipations-request/').view_name, 'request_antecipations_list')

    def test_log_transactions_url(self):
        self.assertEqual(reverse('log_transactions_list'), '/logs/')
        self.assertEqual(resolve('/logs/').view_name, 'log_transactions_list')


class TestAntecipationView(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email='user@test.com')

    def test_antecipations_list_view_anonymous_302(self):
        response = self.client.get('/antecipations/')
        self.assertEqual(response.status_code, 302)

    def test_antecipations_list_view_authenticated_200(self):
        self.client.force_login(self.user)
        response = self.client.get('/antecipations/')
        self.assertEqual(response.status_code, 200)

    def test_antecipations_request_list_view_anonymous_302(self):
        response = self.client.get('/antecipations-request/')
        self.assertEqual(response.status_code, 302)

    def test_antecipations_request_list_view_authenticated_200(self):
        self.client.force_login(self.user)
        response = self.client.get('/antecipations-request/')
        self.assertEqual(response.status_code, 200)

    def test_logs_list_view_anonymous_302(self):
        response = self.client.get('/logs/')
        self.assertEqual(response.status_code, 302)

    def test_logs_list_view_authenticated_200(self):
        self.client.force_login(self.user)
        response = self.client.get('/logs/')
        self.assertEqual(response.status_code, 200)
