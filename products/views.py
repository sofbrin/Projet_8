from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.template import loader
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse

from products.models import ProductDb, UserPersonalDb


def index(request):
    template = loader.get_template('products/index.html')
    return HttpResponse(template.render(request=request))


"""def home(request):
    template = loader.get_template('products/index.html')
    return HttpResponse(template.render(request=request))"""


def results(request):
    query = request.GET.get('query')
    #product = get_object_or_404()
    product = ProductDb.objects.filter(name__icontains=query).order_by('name').first()
    substitutes_list = ProductDb.objects.filter(category=product.category, nutriscore__lt=product.nutriscore).order_by('nutriscore')

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
            #'user_substitutions': request.user.substitutes,
            'page_number': page_number,
    }
    return render(request, 'products/results.html', context)


@login_required
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
        return HttpResponseRedirect(reverse('results') + '?query=' + query + '&page=' + page_number)


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
