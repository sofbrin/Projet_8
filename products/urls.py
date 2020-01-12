from django.urls import path
from . import views


urlpatterns = [
    path('results', views.results, name='results'),
    path('substitute', views.substitute, name='substitute'),
    path('my_substitutes', views.my_substitutes, name='my_substitutes'),
]
