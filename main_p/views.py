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
from django.http import HttpResponseServerError

app_name = 'main_p'
def index(request, user_id):
    api_url = f'http://localhost:8000/main_p/api/{user_id}'  # Use an f-string to format the URL

    # Making a POST request to the API
    api_response = requests.get(api_url)
    api_response = api_response.json()

    user_info = api_response.get('user')

    #輸入假資訊讓網頁顯示
    if request.method == 'POST':
        #改變html中按鈕的value可以達到按下不同按鈕後，跳轉到不同的頁面
        if request.POST.get('button') == 'self_info':
            return redirect('self_info:index', user_id=user_id)
        elif request.POST.get('button') == 'sale_order':
            return redirect('order:sale_order', user_id=user_id)
        elif request.POST.get('button') == 'want_order':
            return redirect('order:want_order', user_id=user_id)
    return render(request, 'main_p/index.html', {'user_id': user_id})

def new_create_order(request, user_id):
    return render(request, 'main_p/new_create_order.html', {'user_id': user_id})

def create_sale_order(request, user_id):
    if request.method == 'POST':
        isbn_input = request.POST.get('ISBN')
        isbns = isbn_input.split('、') if isbn_input else []
        price_input = request.POST.get('Price')
        prices = price_input.split('、') if price_input else []
        description_input = request.POST.get('Description')
        descriptions = description_input.split('、') if description_input else []

        detail_require = 0
        detail_isbn = []
        for isbn in isbns:
        # Check if the ISBN already exists in the database
            book_exists = Book.objects.filter(isbn=isbn).exists()
            if not book_exists:
                detail_require += 1
                detail_isbn.append(isbn)
        if detail_require > 0:
            # If there are ISBNs that require additional information, redirect to book_detail
            return redirect('main_p:book_detail', user_id=user_id, isbns="、".join(detail_isbn))
        # return redirect('main_p:book_detail', user_id=user_id, isbn=isbn)

        # If all forms are valid, you can redirect or perform other actions here
        # return redirect('self_info:personal_order', user_id=user_id)

    #else:
        # formset = SaleOrderFormset()

    return render(request, 'main_p/create_saleOrder.html', {'user_id': user_id})


def create_want_order(request, user_id):
    if request.method == 'POST':
        isbn_input = request.POST.get('ISBN')
        isbns = isbn_input.split('、') if isbn_input else []
        description_input = request.POST.get('Description')
        descriptions = description_input.split('、') if description_input else []

        detail_require = 0
        detail_isbn = []
        for isbn in isbns:
        # Check if the ISBN already exists in the database
            book_exists = Book.objects.filter(isbn=isbn).exists()
            if not book_exists:
                detail_require += 1
                detail_isbn.append(isbn)
        if detail_require > 0:
            # If there are ISBNs that require additional information, redirect to book_detail
            return redirect('main_p:book_detail', user_id=user_id, isbns="、".join(detail_isbn))
    return render(request, 'main_p/create_buyOrder.html', {'user_id': user_id})

def book_detail(request, user_id, isbns):
    isbns_list = isbns.split('、') if isbns else []
    # return redirect('self_info:personal_order', user_id=user_id)
    return render(request, 'main_p/book_detail.html', {'user_id': user_id, 'isbns': isbns_list})


def search(request, user_id):
    if request.method == 'POST':
        api_url = f'http://localhost:8000/main_p/api/search/{user_id}'
        order_type = request.POST.get('order_type')
        category = request.POST.get('category')
        keyword = request.POST.get('keyword')

        form_data = {"order_type": order_type,
                     "category": category,
                     "keyword": keyword
                    }

        api_response = requests.post(api_url, json=form_data)
        api_response = api_response.json()
        orders = api_response.get('orders')
        # Process form data and save to the database
        return render(request, 'main_p/search_result.html', {'orders': orders, 'user_id': user_id})
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
    api_url = f'http://localhost:8000/main_p/api/{user_id}'  # Use an f-string to format the URL

    if request.method == 'POST':
        # Process form data and save to the database
        # If you need to make a POST request, use requests.post()
        api_response = requests.post(api_url, data=request.POST)
    else:
        # Making a GET request to the API
        api_response = requests.get(api_url)

    api_data = api_response.json()
    user_info = api_data.get('user')

    return render(request, 'self_info/index.html', {'user_id': user_id, 'user_info': user_info})
