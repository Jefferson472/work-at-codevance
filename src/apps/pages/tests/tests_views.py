from django.test import TestCase

from apps.core.models import CustomUser


class TestHomePageViews(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email='user@test.com')

    def test_home_page_view_anonymous_302(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_home_page_view_authenticated_200(self):
        self.client.force_login(self.user)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


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
