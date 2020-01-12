
import requests
from django.core.exceptions import ObjectDoesNotExist
from products.models import CategoryDb, ProductDb


def select_categories():
    if CategoryDb.objects.all().count() != 0:
        return
    r_categories = requests.get('https://fr.openfoodfacts.org/categories.json')
    response = r_categories.json()
    categories = response['tags']

    selected_categories = []

    """ sorting categories by size (reverse = from the biggest to the smallest """
    categories = sorted(categories, key=lambda x: x['products'], reverse=True)
    for category in categories:
        try:
            CategoryDb.objects.get(url=category['url'])
        except ObjectDoesNotExist:
            selected_categories.append(category)
            save_categories_in_db(category)
            print('\nLa catégorie "' + category['name'] + '" vient d\'être ajoutée dans la base de données')
            select_products(category)
            if len(selected_categories) == 20:
                break


def select_products(category):
    selected_products = []
    page = 1

    while len(selected_products) < 20:
        r_products = requests.get(category['url'] + '/{}.json'.format(page))
        response = r_products.json()
        products = response['products']

        for product in products:
            try:
                ProductDb.objects.get(url=product['url'])
            except ObjectDoesNotExist:
                if 'product_name' in product and product['product_name'] != '' \
                        and 'url' in product and product['url'] != '' \
                        and 'nutrition_grades' in product and product['nutrition_grades'] != '' \
                        and 'fat_100g' in product and product['fat_100g'] != '' \
                        and 'saturated_fat_100g' in product and product['saturated_fat_100g'] != '' \
                        and 'sugars_100g' in product and product['sugars_100g'] != '' \
                        and 'salt_100g' in product and product['salt_100g'] != '':
                    selected_products.append(product)
                    save_products_in_db(product, category)
                    print('Le produit "' + product['product_name'] + '" vient d\'être ajouté dans cette catégorie.')
                if len(selected_products) == 20:
                    break
        page += 1


def save_categories_in_db(category):
    category_db = CategoryDb(url=category['url'], name=category['name'])
    category_db.save()


def save_products_in_db(product, category):
    category_db = CategoryDb.objects.get(url=category['url'])

    product_db = ProductDb(name=product['product_name'].encode(encoding='UTF-8'), category=category_db,
                           url=product['url'].encode(encoding='UTF-8'),
                           nutriscore=product['nutrition_grades'],
                           fat=product['fat_100g'].encode(encoding='UTF-8'),
                           saturated_fat=product['saturated_fat_100g'].encode(encoding='UTF-8'),
                           sugar=product['sugars_100g'].encode(encoding='UTF-8'),
                           salt=product['salt_100g'].encode(encoding='UTF-8'))
    product_db.save()
