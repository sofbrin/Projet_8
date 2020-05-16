from selenium import webdriver
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from django.test import TestCase
from django.urls import reverse
from users.forms import RegistrationForm, LoginForm
from users.models import User


class SeleniumTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome(ChromeDriverManager().install())
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        User.objects.create_user(email='jLennon@gmail.com', password='john1234')

    def test_signup_right_info(self):
        self.selenium.get(self.live_server_url + '/users/signup')
        first_name = self.selenium.find_element(By.NAME, 'first_name')
        last_name = self.selenium.find_element(By.NAME, 'last_name')
        email1 = self.selenium.find_element(By.NAME, 'email')
        password1 = self.selenium.find_element(By.NAME, 'password1')
        password2 = self.selenium.find_element(By.NAME, 'password2')
        submit = self.selenium.find_element(By.ID, "logforms")
        first_name.send_keys('Robert')
        last_name.send_keys('Redford')
        email1.send_keys('rob@gmail.com')
        password1.send_keys('robert1234')
        password2.send_keys('robert1234')
        submit.click()
        self.assertEqual(self.selenium.current_url, self.live_server_url + '/')

    def test_signup_wrong_email(self):
        self.selenium.get(self.live_server_url + '/users/signup')
        first_name = self.selenium.find_element(By.NAME, 'first_name')
        last_name = self.selenium.find_element(By.NAME, 'last_name')
        email1 = self.selenium.find_element(By.NAME, 'email')
        password1 = self.selenium.find_element(By.NAME, 'password1')
        password2 = self.selenium.find_element(By.NAME, 'password2')
        submit = self.selenium.find_element(By.ID, "logforms")
        first_name.send_keys('George')
        last_name.send_keys('Clooney')
        email1.send_keys('georgegmail.com')
        password1.send_keys('george1234')
        password2.send_keys('george1234')
        submit.click()
        try:
            error_email = self.selenium.find_element(By.XPATH, '//*[text()="Saisissez une adresse de courriel valide."]')
        except NoSuchElementException:
            self.fail('Impossible de trouver le message d\'erreur')
        self.assertTrue(error_email.is_displayed())

    def test_signup_wrong_password(self):
        self.selenium.get(self.live_server_url + '/users/signup')
        first_name = self.selenium.find_element(By.NAME, 'first_name')
        last_name = self.selenium.find_element(By.NAME, 'last_name')
        email1 = self.selenium.find_element(By.NAME, 'email')
        password1 = self.selenium.find_element(By.NAME, 'password1')
        password2 = self.selenium.find_element(By.NAME, 'password2')
        submit = self.selenium.find_element(By.ID, "logforms")
        first_name.send_keys('Brad')
        last_name.send_keys('Pitt')
        email1.send_keys('brad@gmail.com')
        password1.send_keys('brad1234')
        password2.send_keys('brad123')
        submit.click()
        try:
            error_email = self.selenium.find_element(By.XPATH, '//*[text()="Les mots de passe ne correspondent pas. '
                                                              'Veuillez les saisir à nouveau."]')
        except NoSuchElementException:
            self.fail('Impossible de trouver le message d\'erreur')
        self.assertTrue(error_email.is_displayed())

    def test_login_right_info(self):
        self.selenium.get(self.live_server_url + '/users/login')
        email = self.selenium.find_element(By.NAME, 'email')
        password = self.selenium.find_element(By.NAME, 'password')
        submit = self.selenium.find_element(By.ID, "logforms")
        email.send_keys('jLennon@gmail.com')
        password.send_keys('john1234')
        submit.click()
        self.assertEqual(self.selenium.current_url, self.live_server_url + '/')

    def test_login_wrong_email_and_or_password(self):
        self.selenium.get(self.live_server_url + '/users/login')
        email = self.selenium.find_element(By.NAME, 'email')
        password = self.selenium.find_element(By.NAME, 'password')
        submit = self.selenium.find_element(By.ID, "logforms")
        email.send_keys('johngmail.com')
        password.send_keys('john1234')
        submit.click()
        try:
            error_email = self.selenium.find_element(By.XPATH, '//*[text()="L\'email et/ou le mot de passe sont '
                                                              'invalides. Veuillez saisir à nouveau vos identifiants '
                                                              'ou créer un compte."]')
        except NoSuchElementException:
            self.fail('Impossible de trouver le message d\'erreur')
        self.assertTrue(error_email.is_displayed())


class TestModelsUserManager(TestCase):
    def test_username_is_email(self):
        self.assertEqual(User.USERNAME_FIELD, 'email')

    def test_create_manager(self):
        user = User.objects.create_user('arthurH@gmail.com', '1234', first_name='Arthur')
        self.assertEqual(user.email, 'arthurH@gmail.com')
        self.assertEqual(user.first_name, 'Arthur')

    def test_create_superuser(self):
        superuser = User.objects.create_superuser('arthurH@gmail.com', '1234',  first_name='Arthur')
        self.assertEqual(superuser.email, 'arthurH@gmail.com')
        self.assertEqual(superuser.first_name, 'Arthur')
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)


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
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)

    def test_logout_ok(self):
        self.client.login(username='arthurH@gmail.com', password='1234')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)

    def test_account_returns_200(self):
        self.client.login(username='arthurH@gmail.com', password='1234')
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)

    def test_account_without_login(self):
        self.client.logout()
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 302)
