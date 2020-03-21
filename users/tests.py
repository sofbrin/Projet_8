from django.test import TestCase
from django.urls import reverse
from products.models import User
from users.forms import RegistrationForm, LoginForm


# Create your tests here.

class TestViewsUsers(TestCase):

    """def setUp(self):
        User.objects.create(first_name='Arthur', last_name='H', email='arthurH@gmail.com')
        self.user = User.objects.get(email='arthurH@gmail.com')
        self.user.set_password('1234')
        self.user.save()"""

    def test_registration_returns_200(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_registration_post(self):
        payloads = {'first_name': 'Arthur',
                    'last_name': 'H',
                    'email': 'arthurH@gmail.com',
                    'password': '1234'}
        response = self.client.post(reverse('signup'), payloads)
        self.assertEqual(response.status_code, 200)

    def test_login_returns_302(self):
        payloads = {'username': 'Arthur',
                    'password': '1234'}
        print(payloads)
        response = self.client.post(reverse('login'), payloads)
        self.assertEqual(response.status_code, 302)

    def test_logout_returns_302(self):
        self.client.login(username='arthurH@gmail.com', password='1234')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_account_returns_200(self):
        self.client.login(username='arthurH@gmail.com', password='1234')
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)



