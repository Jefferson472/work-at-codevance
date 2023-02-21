from django.test import TestCase
from django.urls import resolve, reverse


class TestCandidateUrls(TestCase):
    def test_home_page_url(self):
        self.assertEqual(reverse('home_page'), '/')
        self.assertEqual(resolve('/').view_name, 'home_page')
