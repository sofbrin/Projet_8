from django.test import TestCase
from django.urls import reverse
from products.models import User
from users.forms import RegistrationForm, LoginForm


# Create your tests here.


class RegistrationFormTest(TestCase):
    def setUp(self):
        self.form = RegistrationForm()


class RegisterTest(TestCase):
    pass


class LoginTest(TestCase):
    pass


class LogoutTest(TestCase):
    pass


class AccountTest(TestCase):
    def setUp(self):
        User.objects.create(first_name='Arthur', last_name='H', email='arthurH@gmail.com')
        self.user = User.objects.get(email='arthurH@gmail.com')
        self.user.set_password('1234')
        self.user.save()

    def test_account_returns_200(self):
        self.client.login(username='arthurH@gmail.com', password='1234')
        response = self.client.get(reverse('account'))
        print(response)
        htmlTest = response.content
        print(htmlTest)
        self.assertEqual(response.status_code, 200)
        #self.assertHTMLEqual('<h1 class="text-uppercase font-weight-bold">Arthur</h1>', html)


