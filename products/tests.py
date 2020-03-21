import unittest
import json
from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth.decorators import login_required
from psycopg2.extensions import JSON

from products.models import ProductDb, CategoryDb, UserPersonalDb
from users.models import User

# Create your tests here.


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


class TestViewsProducts(TestCase):

    def setUp(self):
        self.user = User.objects.create(first_name='Arthur', last_name='H', email='arthurH@gmail.com')
        self.user.set_password('1234')
        self.user.save()
        self.category = CategoryDb.objects.create(name='pâte à tartiner', url='')
        self.product = ProductDb.objects.create(name='nutella', url='', image='', nutriscore='d', fat=0, saturated_fat=0,
                                 sugar=0, salt=0, category=self.category)
        self.substitute1 = ProductDb.objects.create(name='nutella bio', url='', image='', nutriscore='a', fat=0, saturated_fat=0,
                                 sugar=0, salt=0, category=self.category)
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
        print(response)

    def test_my_substitutes_returns_300_user_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('my_substitutes'))
        self.assertEqual(response.status_code, 302)
        print(response)

    def test_results_returns_better_nutriscore(self):
        product = self.product
        response = self.client.post(reverse('results'), {'query': product.name})
        context = response.context
        substitutes = context['substitutes'][:]
        print(substitutes)
        for substitute in substitutes:
            self.assertLess(substitute.nutriscore, product.nutriscore)
            print(substitute.nutriscore, product.nutriscore)

    def test_results_pagination_returns_6_substitutes(self):
        number_of_substitutes = 8
        for substitute in range(number_of_substitutes):
            ProductDb.objects.create(name='subTest', url='', image='', nutriscore='', fat=0, saturated_fat=0, sugar=0,
                                     salt=0, category=self.category)
        response = self.client.get(reverse('results'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('paginate' in response.context)
        self.assertTrue(response.context['paginate'])
        self.assertTrue(len(response.context['substitutes']) == 6)

    def test_results_pagination_returns_page_2(self):
        response = self.client.get(reverse('results')+'?page=2')
        self.assertEqual(response.status_code, 302)
        self.assertTrue('paginate' in response.context)
        self.assertTrue(response.context['paginate'])
        self.assertTrue(len(response.context['substitutes']) == 2)

    def test_results_returns_200(self):
        product = self.product
        response = self.client.post(reverse('results'), {'query': product})
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
        print(original_product, replaced_product)
        previous_db_count = UserPersonalDb.objects.count()
        payloads = {'substitute_id': replaced_product, 'product_id': original_product}
        print(payloads)
        response = self.client.post(reverse('save_in_db'), payloads)
        new_db_count = UserPersonalDb.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(previous_db_count + 1, new_db_count)

    """def test_save_in_db_returns_prod_already_in_db(self):
        #créer userpersonaldb
        original_product = self.product.id
        replaced_product = self.substitute1.id
        self.client.login(username='arthurH@gmail.com', password='1234')
        payloads = {'substitute_id': replaced_product, 'product_id': original_product}
        response = self.client.post(reverse('save_in_db'), payloads)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        print(response_json)
        self.assertTrue(response_json['is_in_db'])"""



