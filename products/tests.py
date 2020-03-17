import unittest
import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from products.models import ProductDb, CategoryDb, UserPersonalDb
from users.models import User


# Create your tests here.


class IndexPageTest(TestCase):
    def test_index_returns_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        

class LegalNoticeTest(TestCase):
    def text_legal_notice_returns_200(self):
        response = self.client.get(reverse('legal_notice'))
        self.assertEqual(response.status_code, 200)


class ProductTest(TestCase):
    def setUp(self):
        CategoryDb.objects.create(name='fromage', url='')
        self.category = CategoryDb.objects.get(name='fromage')
        ProductDb.objects.create(name='comté', url='', image='', nutriscore='', fat=0, saturated_fat=0,
                                 sugar=0, salt=0, category=self.category)
        self.product = ProductDb.objects.get(name='comté')

    def test_product_returns_200(self):
        product_id = self.product.id
        response = self.client.get(reverse('product', args=(product_id, )))
        self.assertEqual(response.status_code, 200)


class MySubstitutesTest(TestCase):
    def setUp(self):
        User.objects.create(first_name='Arthur', last_name='H', email='arthurH@gmail.com')
        self.user = User.objects.get(email='arthurH@gmail.com')
        self.user.set_password('1234')
        self.user.save()

    def test_my_substitutes_user_logged_in(self):
        self.client.login(username='arthurH@gmail.com', password='1234')
        response = self.client.get(reverse('my_substitutes'))
        self.assertEqual(response.status_code, 200)
        print(response)

    def test_my_substitutes_user_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('my_substitutes'))
        self.assertEqual(response.status_code, 302)
        print(response)


class ResultsTestCase(TestCase):
    def setUp(self):
        User.objects.create(first_name='Arthur', last_name='H', email='arthurH@gmail.com')
        self.user = User.objects.get(email='arthurH@gmail.com')
        self.user.set_password('1234')
        self.user.save()

        CategoryDb.objects.create(name='pâte à tartiner', url='')
        self.category = CategoryDb.objects.get(name='pâte à tartiner')
        ProductDb.objects.create(name='nutella', url='', image='', nutriscore='d', fat=0, saturated_fat=0,
                                 sugar=0, salt=0, category=self.category)
        self.product = ProductDb.objects.get(name='nutella')
        ProductDb.objects.create(name='nutella bio', url='', image='', nutriscore='a', fat=0, saturated_fat=0,
                                 sugar=0, salt=0, category=self.category)
        ProductDb.objects.create(name='pâte noisette', url='', image='', nutriscore='b', fat=0, saturated_fat=0,
                                 sugar=0, salt=0, category=self.category)
        ProductDb.objects.create(name='pâte choco', url='', image='', nutriscore='e', fat=0, saturated_fat=0,
                                 sugar=0, salt=0, category=self.category)

    def test_results_returns_better_nutriscore(self):
        """ testing that search's result has a better nutriscore than original product """
        product = self.product
        substitutes_list = ProductDb.objects.filter(category=product.category,
                                                    nutriscore__lt=product.nutriscore)
        print(substitutes_list)
        for substitute in substitutes_list:
            self.assertLess(substitute.nutriscore, product.nutriscore)

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


class SaveInDbTest(TestCase):
    def setUp(self):
        User.objects.create(first_name='Arthur', last_name='H', email='arthurH@gmail.com')
        self.user = User.objects.get(email='arthurH@gmail.com')
        self.user.set_password('1234')
        self.user.save()

        CategoryDb.objects.create(name='pâte à tartiner', url='')
        self.category = CategoryDb.objects.get(name='pâte à tartiner')
        ProductDb.objects.create(name='nutella', url='', image='', nutriscore='d', fat=0, saturated_fat=0,
                                 sugar=0, salt=0, category=self.category)
        self.product = ProductDb.objects.get(name='nutella')
        ProductDb.objects.create(name='nutella bio', url='', image='', nutriscore='a', fat=0, saturated_fat=0,
                                 sugar=0, salt=0, category=self.category)
        self.substitute = ProductDb.objects.get(name='nutella bio')

    def test_save_in_db_returns_200(self):
        original_product = self.product
        replaced_product = self.substitute
        user = self.user
        UserPersonalDb.objects.create(original_product=original_product, replaced_product=replaced_product, user=user)
        data = {'original_product': 'nutella', 'replaced_product': 'nutella bio', 'user': 'arthurH@gmail.com'}
        response = self.client.post(reverse('results'), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

    def test_save_in_db_returns_prod_already_in_db(self):
        pass

