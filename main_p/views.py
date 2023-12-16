from django.shortcuts import render,redirect
from django.http import HttpResponse
import requests
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from main_p.models import Book
# from .forms import SaleOrderFormset
from .forms import SaleOrderForm
from .forms import BuyOrderForm
from django.forms import formset_factory, BaseFormSet

app_name = 'main_p'
def index(request, user_id):
    fake_user = {'user_id': user_id, 'user_name': 'Jerry', 'role': 'user'}
    #輸入假資訊讓網頁顯示
    if request.method == 'POST':
        #改變html中按鈕的value可以達到按下不同按鈕後，跳轉到不同的頁面
        if request.POST.get('button') == 'self_info':
            return redirect('self_info:index', user_id=fake_user['user_id'])
        elif request.POST.get('button') == 'sale_order':
            return redirect('order:sale_order', user_id=fake_user['user_id'])
        elif request.POST.get('button') == 'want_order':
            return redirect('order:want_order', user_id=fake_user['user_id'])
    return render(request, 'main_p/index.html', {'user_id': user_id})

def new_create_order(request, user_id):
    return render(request, 'main_p/new_create_order.html', {'user_id': user_id})

SaleOrderFormset = formset_factory(SaleOrderForm, extra=1)

def create_sale_order(request, user_id):
    if request.method == 'POST':
        formset = SaleOrderFormset(request.POST)

        if formset.is_valid():
            for form in formset:
                isbn = form.cleaned_data.get('isbn')
                price = form.cleaned_data.get('price')
                description = form.cleaned_data.get('description')

                # Check if the ISBN already exists in the database
                book_exists = Book.objects.filter(isbn=isbn).exists()

                if not book_exists:
                    # Store formset management form in the session
                    request.session['formset_management_form'] = formset.management_form.cleaned_data
                    # ISBN doesn't exist, redirect to book_detail page
                    return redirect('main_p:book_detail', user_id=user_id, isbn=isbn)

                # Perform additional actions with the form data if needed
                # For example, save the data to the database or process the order

            # If all forms are valid, you can redirect or perform other actions here
            return redirect('self_info:personal_order', user_id=user_id)  # Adjust this to your needs

    else:
        formset = SaleOrderFormset()

    return render(request, 'main_p/create_saleOrder.html', {'user_id': user_id, 'formset': formset})


BuyOrderFormset = formset_factory(BuyOrderForm, extra=1)
def create_want_order(request, user_id):
    # Your logic for creating want orders
    if request.method == 'POST':
        formset = BuyOrderFormset(request.POST)

        if formset.is_valid():
            for form in formset:
                isbn = form.cleaned_data.get('isbn')
                description = form.cleaned_data.get('description')

                # Check if the ISBN already exists in the database
                #book_exists = Book.objects.filter(isbn=isbn).exists()
                #if not book_exists:
                    # Store formset management form in the session
                    #request.session['formset_management_form'] = formset.management_form.cleaned_data
                    # ISBN doesn't exist, redirect to book_detail page
                return redirect('main_p:create_buyOrder', user_id=user_id)

            return redirect('self_info:personal_order', user_id=user_id)
    else:
        formset = BuyOrderFormset()
    return render(request, 'main_p/create_buyOrder.html', {'user_id': user_id, 'formset': formset})
   
def book_detail(request, user_id, isbn):
    formset_management_form_data = request.session.pop('formset_management_form', None)

    if formset_management_form_data is None:
        return HttpResponseServerError("Formset management form data not found in the session.")

    # Create a new formset with the retrieved management form data
    formset = SaleOrderFormset(initial=formset_management_form_data)

    # Your existing code for handling the book detail page goes here

    return render(request, 'main_p/book_detail.html', {'user_id': user_id, 'isbn': isbn, 'formset': formset})


def search(request, user_id):
    if request.method == 'POST':
        # Process form data and save to the database
        return render(request, 'main_p/search.html', {'user_id': user_id})
    else:
        return render(request, 'main_p/search.html', {'user_id': user_id})
        
def search_result(request, user_id):
    if request.method == 'POST':
        # Process form data and save to the database
        return render(request, 'main_p/search_result.html', {'user_id': user_id})
    else:
        return render(request, 'main_p/search_result.html', {'user_id': user_id})
    
def evaluate_user(request, user_id):
    if request.method == 'POST':
        # Process form data and save to the database
        return render(request, 'evaluate/evaluate_user.html', {'user_id': user_id})
    else:
        return render(request, 'evaluate/evaluate_user.html', {'user_id': user_id})
        
def self_info(request, user_id):
    if request.method == 'POST':
        # Process form data and save to the database
        return render(request, 'self_info/index.html', {'user_id': user_id})
    else:
        return render(request, 'self_info/index.html', {'user_id': user_id})
        