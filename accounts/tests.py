from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your tests here.
class SignUpPageTests(TestCase):
    
    username = 'testuser'
    email = 'test@email.com'
    password = 'secretpassword123'

    def test_signup_url_by_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_signup_template_name_correct(self):
        response = self.client.get(reverse('signup'))
        self.assertTemplateUsed(response, 'accounts/signup.html')

    def test_signup_form(self):
        new_user = get_user_model().objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, self.username)
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)


class LoginPageTests(TestCase):

    def test_login_url_by_name(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_template_name_correct(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'accounts/login.html')