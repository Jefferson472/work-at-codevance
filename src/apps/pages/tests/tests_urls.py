from django.test import TestCase
from django.urls import resolve, reverse


class TestUrls(TestCase):
    def test_home_page_url(self):
        self.assertEqual(reverse('home_page'), '/')
        self.assertEqual(resolve('/').view_name, 'home_page')

    def test_payments_url(self):
        self.assertEqual(reverse('payments_list'), '/payments/')
        self.assertEqual(resolve('/payments/').view_name, 'payments_list')
