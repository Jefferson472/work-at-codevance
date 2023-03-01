from django.test import TestCase
from django.urls import resolve, reverse

from apps.core.models import CustomUser


class TestUrls(TestCase):
    def test_home_page_url(self):
        self.assertEqual(reverse('home_page'), '/')
        self.assertEqual(resolve('/').view_name, 'home_page')


class TestHomePageViews(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email='user@test.com')

    def test_home_page_view_anonymous_302(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_home_page_view_authenticated_200(self):
        self.client.force_login(self.user)
        response = self.client.get('/')
        self.assertRedirects(response, '/payments/')
