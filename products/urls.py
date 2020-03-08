from django.urls import path
from . import views


urlpatterns = [
    path('results', views.results, name='results'),
    path('product/<product_id>/', views.detail, name='product'),
    path('my_substitutes/', views.my_substitutes, name='my_substitutes'),
    path('results/save_in_db/', views.save_in_db, name='save_in_db'),
    path('autocomplete/', views.autocompleteModel, name='autocomplete'),
    path('legal_notice/', views.legal_notice, name='legal_notice'),
    # path('results/save_in_db/<substitute_id>/<product_id>/', views.save_in_db, name='save_in_db')
]
