# forms.py
"""
from django import forms
from django.forms import formset_factory

class SaleOrderForm(forms.Form):
    isbn = forms.CharField(label='ISBN', required=True)
    price = forms.DecimalField(label='Price', required=True)
    description = forms.CharField(label='Description', required=False, widget=forms.Textarea)

SaleOrderFormset = formset_factory(SaleOrderForm, extra=1)
"""
# forms.py
from django import forms

class SaleOrderForm(forms.Form):
    isbn = forms.CharField(label='ISBN', required=True)
    price = forms.DecimalField(label='Price', required=True)
    description = forms.CharField(label='Description', required=False, widget=forms.Textarea)
    
class BuyOrderForm(forms.Form):
    isbn = forms.CharField(label='ISBN', required=True)
    description = forms.CharField(label='Description', required=False, widget=forms.Textarea)
