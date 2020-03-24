from django.test import TestCase
from django.urls import reverse
from users.forms import RegistrationForm, LoginForm
from users.models import User


class TestFormsUsers(TestCase):

    def setUp(self):
        self.payloads1 = {
            'first_name': 'Arthur',
            'last_name': 'H',
            'email': 'arthurH@gmail.com',
            'password1': '1234',
            'password2': '1234'
        }
        self.payloads2 = {
            'email': 'arthurH@gmail.com',
            'password': '1234'
        }

    def test_regForm_is_valid(self):
        data = self.payloads1
        form = RegistrationForm(data)
        self.assertTrue(form.is_valid())

    def test_logForm_is_valid(self):
        data = self.payloads2
        form = LoginForm(data)
        self.assertTrue(form.is_valid())


class TestViewsUsers(TestCase):

    def setUp(self):
        self.user = User.objects.create(first_name='Arthur', last_name='H', email='arthurH@gmail.com')
        self.payloads = {'username': 'arthurH@gmail.com', 'password': '1234'}

    def test_registration_returns_200(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_registration_post(self):
        response = self.client.post(reverse('signup'))
        checked_user = User.objects.first()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(checked_user.first_name, self.user.first_name)

    def test_login_ok(self):
        self.client.logout()
        payloads = self.payloads
        response = self.client.post(reverse('login'), payloads, follow=True)
        print(response)
        #self.assertEqual(response.status_code, 302)
        #self.assertEqual(response.url, 'home')
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)

    def test_logout_ok(self):
        self.client.login(username='arthurH@gmail.com', password='1234')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)

    def test_account_returns_200(self):
        self.client.login(username='arthurH@gmail.com', password='1234')
        print(self.user)
        response = self.client.get(reverse('account'))
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_account_without_login(self):
        self.client.logout()
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 302)
