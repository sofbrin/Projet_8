from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from products.models import ProductDb, HistoricDb


def index(request):
    template = loader.get_template('products/index.html')
    return HttpResponse(template.render(request=request))


"""def home(request):
    template = loader.get_template('products/index.html')
    return HttpResponse(template.render(request=request))"""


def results(request):
    query = request.GET.get('query')
    product = ProductDb.objects.get(name__icontains=query)
    substitutes_list = ProductDb.objects.filter(category=product.category, nutriscore__lt=product.nutriscore).order_by('nutriscore')

    paginator = Paginator(substitutes_list, 6)
    page = request.GET.get('page')

    try:
        substitutes = paginator.page(page)
        context = {
            'substitutes': substitutes,
            'paginate': True,
            'page_title': query,
        }
    except PageNotAnInteger:
        context = paginator.page(1)
    except EmptyPage:
        context = paginator.page(paginator.num_pages)

    return render(request, 'product/results.html', context)


@login_required
def save_substitute_in_db(request, substitute, product):

    historic_db = HistoricDb(product_replaceable=substitute, product_original=product)
    historic_db.save()


def substitute(request):
    template = loader.get_template('products/substitute.html')
    return HttpResponse(template.render(request=request))


def my_substitutes(request):
    template = loader.get_template('products/my_substitutes.html')
    return HttpResponse(template.render(request=request))
