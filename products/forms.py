from django.forms import ModelForm, TextInput
from django.forms.utils import ErrorList
from django import forms

from .models import ProductDb


class ProductSearch(ModelForm):
    name = forms.CharField(required=True)

    class Meta:
        model = ProductDb
        fields = ['name']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'})
        }
