from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import get_user_model

class SignupPageTests(TestCase):
    username = 'newuser'
    email = 'newuser@email.com'
    def test_signup_page_status_code(self):
        response = self.client.get('/users/register/')
        self.assertEqual(response.status_code, 200)
    def test_view_url_by_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cancer/base.html')
    def test_signup_form(self):
        new_user = get_user_model().objects.create_user(
        self.username, self.email)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()
        [0].username, self.username, )
        self.assertEqual(get_user_model().objects.all()
        [0].email, self.email)

class cancerHomePageTests(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get('/cancer/')
        self.assertEquals(response.status_code, 302)
    def test_view_url_by_name(self):
        response = self.client.get(reverse('cancer-home'))
        self.assertEquals(response.status_code, 302)
    # def test_view_uses_correct_template(self):
    #     response = self.client.get(reverse('cancer-home'))
    #     self.assertEquals(response.status_code, 302)
    #     self.assertTemplateUsed(response, 'cancer/home.html')
        

