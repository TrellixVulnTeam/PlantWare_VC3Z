from django.forms import ModelForm
from .models import *


class ProductAddForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'description', 'image', 'available']



class CustomerUpdateForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']


class ProductionPlanForm(ModelForm):
    class Meta:
        model = Production
        fields = ['product', 'quantity']

