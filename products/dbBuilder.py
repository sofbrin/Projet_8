import requests
from django.core.exceptions import ObjectDoesNotExist
from products.models import CategoryDb, ProductDb


def select_categories(limit_cat):
    if CategoryDb.objects.all().count() != 0:
        return

    response = requests.get('https://fr.openfoodfacts.org/categories.json')
    data = response.json()
    categories = data['tags']
    selected_cat = categories[:limit_cat]
    for category in selected_cat:
        CategoryDb.objects.create(url=category['url'], name=category['name'])
        print('\nLa catégorie "' + category['name'] + '" vient d\'être ajoutée dans la base de données'
                                                      ' avec les produits suivants :')
        select_products(category)


def select_products(category):
    selected_prod = []
    page = 1

    while len(selected_prod) < 20:
        r_products = requests.get('https://world.openfoodfacts.org/cgi/search.pl', params={
            'tagtype_0': 'categories',
            'tag_contains_0': 'contains',
            'tag_0': category['id'],
            'tagtype_1': 'countries',
            'tag_contains_1': 'contains',
            'tag_1': 'france',
            'nutriment_0': 'fat',
            'nutriment_compare_0': 'gte',
            'nutriment_value_O': 0,
            'nutriment_1': 'saturated-fat',
            'nutriment_compare_1': 'gte',
            'nutriment_value_0': 0,
            'nutriment_2': 'sugars',
            'nutriment_compare_2': 'gte',
            'nutriment_value_2': 0,
            'nutriment_3': 'salt',
            'nutriment_compare_3': 'gte',
            'nutriment_value_3': 0,
            'json': 1,
            'sort_by': 'unique_scans_n',
            'page_size': 50,
            'action': 'process',
            'page': page

        })
        response = r_products.json()
        products = response['products']
        for product in products:
            if 'product_name' not in product or product['product_name'] == '':
                continue
            try:
                ProductDb.objects.get(name__iexact=product['product_name'])
            except ObjectDoesNotExist:
                if 'url' in product and product['url'] != '' \
                        and 'nutrition_grades' in product and product['nutrition_grades'] != '':
                    selected_prod.append(product)
                    print(product['product_name'])
                    categorydb = CategoryDb.objects.get(url=category['url'])
                    ProductDb.objects.create(name=product['product_name'], url=product['url'],
                                             image=product['image_front_url'], nutriscore=product['nutrition_grades'],
                                             category=categorydb, fat=product['nutriments']['fat'],
                                             saturated_fat=product['nutriments']['saturated-fat'],
                                             sugar=product['nutriments']['sugars'], salt=product['nutriments']['salt'])
                if len(selected_prod) == 20:
                    break
        page += 1
