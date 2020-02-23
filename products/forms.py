from django.forms import ModelForm, TextInput
from django.forms.utils import ErrorList

from .models import ProductDb


class ProductSearch(ModelForm):
    class Meta:
        model = ProductDb
        fields = ['name']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'})
        }
