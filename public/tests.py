from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase
from django.http import HttpResponseRedirect
from django.urls import reverse

class PublicHomePageTests(SimpleTestCase):
    def test_home_page_status_code(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
    def test_view_url_by_name(self):
        response = self.client.get(reverse('website-home'))
        self.assertEqual(response.status_code, 200)
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('website-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'public/home.html')

        