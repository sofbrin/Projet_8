from selenium import webdriver
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase, TestCase, SimpleTestCase
from django.urls import reverse
from webdriver_manager.chrome import ChromeDriverManager

from products.models import ProductDb, CategoryDb, UserPersonalDb
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

    def test_link_product_redirects_OFF_detail_product(self):
        self.selenium.get('http://127.0.0.1:8000/products/product/352/')
        called_url = 'https://world.openfoodfacts.org/product/3272770003148/pure-goat-chavroux'
        self.selenium.find_element(By.LINK_TEXT, "Voir la fiche sur le site d'Open Food Facts").click()
        self.assertEqual(self.selenium.current_url, called_url)


class TestViewsProducts(TestCase):

    def setUp(self):
        self.user = User.objects.create(first_name='Arthur', last_name='H', email='arthurH@gmail.com')
        self.user.set_password('1234')
        self.user.save()
        self.category = CategoryDb.objects.create(name='pâte à tartiner', url='')
        self.product = ProductDb.objects.create(name='nutella', url='', image='', nutriscore='d', fat=0,
                                                saturated_fat=0, sugar=0, salt=0, category=self.category)
        self.substitute1 = ProductDb.objects.create(name='nutella bio', url='', image='', nutriscore='a', fat=0,
                                                    saturated_fat=0, sugar=0, salt=0, category=self.category)
        ProductDb.objects.create(name='pâte noisette', url='', image='', nutriscore='b', fat=0, saturated_fat=0,
                                 sugar=0, salt=0, category=self.category)
        ProductDb.objects.create(name='pâte choco', url='', image='', nutriscore='e', fat=0, saturated_fat=0,
                                 sugar=0, salt=0, category=self.category)

    def test_product_returns_200(self):
        product_id = self.product.id
        response = self.client.get(reverse('product', args=(product_id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product.html')

    def test_my_substitutes_returns_200_user_logged_in(self):
        self.client.login(username='arthurH@gmail.com', password='1234')
        response = self.client.get(reverse('my_substitutes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/my_substitutes.html')

    def test_my_substitutes_returns_300_user_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('my_substitutes'))
        self.assertEqual(response.status_code, 302)

    def test_results_returns_better_nutriscore(self):
        product = self.product
        response = self.client.get(reverse('results'), {'query': product.name})
        context = response.context
        substitutes = context['substitutes']
        for substitute in substitutes:
            self.assertLess(substitute.nutriscore, product.nutriscore)

    def test_results_returns_200(self):
        product = self.product
        response = self.client.get(reverse('results'), {'query': product})
        self.assertEqual(response.status_code, 200)

    def test_search_returns_nothing(self):
        response = self.client.post(reverse('results'), {'query': ''})
        self.assertEqual(response.status_code, 302)

    def test_search_returns_unknown_product(self):
        product = 'unknown product'
        response = self.client.post(reverse('results'), {'query': product})
        self.assertEqual(response.status_code, 302)

    def test_save_in_db_returns_200(self):
        original_product = self.product.id
        replaced_product = self.substitute1.id
        self.client.login(username='arthurH@gmail.com', password='1234')
        previous_db_count = UserPersonalDb.objects.count()
        data = {'substitute_id': replaced_product, 'product_id': original_product}
        response = self.client.post(reverse('save_in_db'), data)
        new_db_count = UserPersonalDb.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(previous_db_count + 1, new_db_count)

    def test_save_in_db_returns_prod_already_in_db(self):
        original_product = self.product.id
        replaced_product = self.substitute1.id
        self.client.login(username='arthurH@gmail.com', password='1234')
        previous_db_count = UserPersonalDb.objects.count()
        data = {'substitute_id': replaced_product, 'product_id': original_product}
        response = self.client.post(reverse('save_in_db'), data)
        response_json = response.json()
        new_db_count = UserPersonalDb.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_json['is_created'])
        self.assertEqual(previous_db_count + 1, new_db_count)
        response2 = self.client.post(reverse('save_in_db'), data)
        response2_json = response2.json()
        last_db_count = UserPersonalDb.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response2_json['is_in_db'])
        self.assertEqual(new_db_count, last_db_count)


class IndexPageTest(SimpleTestCase):
    def test_index_returns_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/index.html')


class LegalNoticeTest(SimpleTestCase):
    def test_legal_notice_returns_200(self):
        response = self.client.get(reverse('legal_notice'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/legal_notice.html')
