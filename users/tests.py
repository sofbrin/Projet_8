from django.test import TestCase
from django.urls import reverse
from users.forms import RegistrationForm, LoginForm
from users.models import UserManager, User


class TestModelsUsers(TestCase):
    def test_username_is_email(self):
        self.assertEqual(User.USERNAME_FIELD, 'email')

    def test_create_manager(self):
        user = User.objects.create_user('arthurH@gmail.com', '1234', first_name='Arthur')
        self.assertEqual(user.email, 'arthurH@gmail.com')
        self.assertEqual(user.first_name, 'Arthur')


class TestFormsUsers(TestCase):

    def setUp(self):
        self.data1 = {
            'first_name': 'Arthur',
            'last_name': 'H',
            'email': 'arthurH@gmail.com',
            'password1': '1234',
            'password2': '1234'
        }
        self.data2 = {
            'email': 'arthurH@gmail.com',
            'password': '1234'
        }

    def test_regForm_is_valid(self):
        data = self.data1
        form = RegistrationForm(data)
        self.assertTrue(form.is_valid())

    def test_logForm_is_valid(self):
        data = self.data2
        form = LoginForm(data)
        self.assertTrue(form.is_valid())


class TestViewsUsers(TestCase):

    def setUp(self):
        self.user = User.objects.create(first_name='Arthur', last_name='H', email='arthurH@gmail.com')
        self.user.set_password('1234')
        self.user.save()
        self.data = {'email': 'arthurH@gmail.com', 'password': '1234'}


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
        data = self.data
        response = self.client.post(reverse('login'), data, follow=True)
        print(response.status_code)
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)

    def test_logout_ok(self):
        self.client.login(username='arthurH@gmail.com', password='1234')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)

    def test_account_returns_200(self):
        test = self.client.login(username='arthurH@gmail.com', password='1234')
        print('TOTO', test)
        print(self.user)
        response = self.client.get(reverse('account'))
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_account_without_login(self):
        self.client.logout()
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 302)
