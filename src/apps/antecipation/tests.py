import random
import string

from django.test import TestCase
from django.urls import resolve, reverse

from apps.antecipation.models import Antecipation, LogTransactions, RequestAntecipation
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
            requester=self.user_operator
        )


class RequestAntecipationTestCase(BaseTestCase):
    def test_request_antecipation_str(self):
        self.assertEqual(str(self.request_antecipation), f'{self.payment} - Aguardando avaliação')

    def test_request_antecipation_status_choices(self):
        self.assertEqual(self.request_antecipation.get_status_display(), 'Aguardando avaliação')


class AntecipationModelTestCase(BaseTestCase):
    def test_antecipation_creation(self):
        Antecipation.objects.create(
            operator=self.operator,
            request_antecipation=self.request_antecipation,
            fee=5.00
        )
        self.assertEqual(Antecipation.objects.count(), 1)


class LogTransactionsModelTestCase(BaseTestCase):
    def test_log_transactions_creation(self):
        LogTransactions.objects.create(
            operator=self.operator,
            request=self.request_antecipation,
            status_after="approved",
            value_before=100.0,
            value_after=90.0
        )
        self.assertEqual(LogTransactions.objects.count(), 1)


class TestUrls(TestCase):
    def test_antecipation_url(self):
        self.assertEqual(reverse('antecipations_list'), '/antecipations/')
        self.assertEqual(resolve('/antecipations/').view_name, 'antecipations_list')


class TestAntecipationListView(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email='user@test.com')

    def test_payment_list_view_anonymous_302(self):
        response = self.client.get('/antecipations/')
        self.assertEqual(response.status_code, 302)

    def test_payment_list_view_authenticated_200(self):
        self.client.force_login(self.user)
        response = self.client.get('/antecipations/')
        self.assertEqual(response.status_code, 200)
