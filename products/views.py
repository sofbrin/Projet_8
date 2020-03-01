import json
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.template import loader
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from products.models import ProductDb, UserPersonalDb
from products.forms import ProductSearch


def autocompleteModel(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        search_qs = ProductDb.objects.filter(name__istartswith=q)[:20]
        results = []
        for p in search_qs:
            results.append(p.name)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def index(request):
    template = loader.get_template('products/index.html')
    return HttpResponse(template.render(request=request))


def results(request):
    query = request.GET.get('query')
    if query == '':
        messages.error(request, 'Vous n\'avez saisi aucun produit', extra_tags='toaster')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        try:
            product = ProductDb.objects.filter(name__icontains=query).order_by('name').first()
            substitutes_list = ProductDb.objects.filter(category=product.category,
                                                        nutriscore__lt=product.nutriscore).order_by('nutriscore')
            paginator = Paginator(substitutes_list, 6)
            page_number = request.GET.get('page')

            try:
                substitutes = paginator.page(page_number)
            except PageNotAnInteger:
                substitutes = paginator.page(1)
            except EmptyPage:
                substitutes = paginator.page(paginator.num_pages)
            context = {
                'product': product,
                'substitutes': substitutes,
                'paginate': True,
                'query': query,
                # 'user_substitutions': request.user.substitutes,
                'page_number': page_number,
            }
            return render(request, 'products/results.html', context)
        except AttributeError:
            messages.error(request, 'Produit inconnu, faites une autre recherche', extra_tags='toaster')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))







    #if request.method == 'GET':
        #form = ProductSearch()
        #return render(request, 'products/results.html', {'form': form})

    #if request.method == 'POST':
        #form = ProductSearch(request.POST)
        #if form.is_valid():
            #name = form.cleaned_data['name']
            #"roductDb.objects.filter(name=name)


            #if post_product is None:
                #messages.warning(request, 'Produit inconnu, faites une autre recherche')



            #else:
                #messages.warning(request, 'Produit inconnu, faites une autre recherche')
                #print('toto 1')
                #return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        #else:
            #messages.warning(request, 'Aucun produit saisi, recommencez')
            #print('toto 2')
            #return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            #try:
                #name = form.cleaned_data['name']
                #ProductDb.objects.filter(name=name)
                #query = request.GET.get('product')

            #except AttributeError:
                #messages.warning(request, 'Produit inconnu, faites une autre recherche')
                #print('toto 1')
                #return HttpResponseRedirect(request.META.get('HTTP_REFERER'))"""

"""@login_required
def save_in_db(request, substitute_id, product_id, query, page_number):
    substitute = ProductDb.objects.get(pk=substitute_id)
    product = ProductDb.objects.get(pk=product_id)
    try:
        UserPersonalDb.objects.get(original_product=product, replaced_product=substitute, user=request.user)
        messages.warning(request, 'Ce produit est déjà dans votre espace personnel')
        return HttpResponseRedirect(reverse('results') + '?query=' + query + '&page=' + page_number)
    except ObjectDoesNotExist:
        UserPersonalDb.objects.create(original_product=product, replaced_product=substitute, user=request.user)
        messages.success(request, 'Le produit a été enregistré dans votre espace personnel')
        return HttpResponseRedirect(reverse('results') + '?query=' + query + '&page=' + page_number)"""


@login_required
@require_http_methods(['POST'])
def save_in_db(request):
    body = json.loads(request.body)
    product_id = body['product_id']
    substitute_id = body['substitute_id']

    original_product = ProductDb.objects.get(pk=product_id)
    replaced_product = ProductDb.objects.get(pk=substitute_id)

    try:
        UserPersonalDb.objects.get(original_product=original_product, replaced_product=replaced_product,
                                   user=request.user)
        messages.error(request, 'Ce produit est déjà dans votre espace', extra_tags='toaster')
        data = {
            'is_in_db': True
        }
    except ObjectDoesNotExist:
        UserPersonalDb.objects.create(original_product=original_product, replaced_product=replaced_product,
                                      user=request.user)
        messages.success(request, 'Ce produit a bien été enregistré')
        data = {
            'is_created': True
        }

    return JsonResponse(data)


def my_substitutes(request):
    substitutes_list = UserPersonalDb.objects.filter(user=request.user)

    paginator = Paginator(substitutes_list, 6)
    page_number = request.GET.get('page')

    try:
        substitutes = paginator.page(page_number)
    except PageNotAnInteger:
        substitutes = paginator.page(1)
    except EmptyPage:
        substitutes = paginator.page(paginator.num_pages)
    context = {
            'substitutes': substitutes,
            'paginate': True,
    }
    return render(request, 'products/my_substitutes.html', context)


def detail(request, product_id):
    product = ProductDb.objects.get(pk=product_id)
    context = {
        'product_id': product.id,
        'product_title_page': product.name,
        'product_image': product.image,
        'product_nutriscore': product.nutriscore,
        'product_fat': product.fat,
        'product_saturated_fat': product.saturated_fat,
        'product_sugar': product.sugar,
        'product_salt': product.salt,
        'product_url': product.url,
    }
    return render(request, 'products/product.html', context)


def legal_notice(request):
    return render(request, 'products/legal_notice.html')
