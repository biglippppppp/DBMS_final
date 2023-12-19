from django.shortcuts import render,redirect
import requests
from main_p.models import SaleOrder
from main_p.models import WantOrder
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.urls import reverse
from django.http import HttpResponseNotAllowed
from itertools import chain



def index(request):
    return render(request, 'order/index.html')


def want_order(request, user_id):
    if request.method == 'GET':
        page = request.GET.get('page', 1)
        # Call the API with the page parameter
        api_url = f'http://localhost:8000/order/api/sale_order/{user_id}/{page}'
        api_response = requests.get(api_url)
        api_data = api_response.json()

        # Get the orders from the API response
        orders = api_data.get('orders', [])
        nested_page_range = api_data.get('page_range')
        int_page = int(page)
        # Flatten the nested lists
        page_range = list(chain.from_iterable(nested_page_range))

        if int_page + 1 <= int(page_range[-1]):
            print('yse')
            next_page = int_page + 1
        else:
            next_page = int_page
        if int_page - 1 >= int(page_range[0]):
            pre_page = int_page - 1
        else:
            pre_page = int_page
        return render(request, 'order/want_order.html', {'orders': orders, 'user_id': user_id, 'page_range': page_range, "current_page": page, "next_page": next_page, "pre_page": pre_page})
    return HttpResponseNotAllowed(['GET'])

def sale_order(request, user_id):
    if request.method == 'GET':
        page = request.GET.get('page', 1)
        # Call the API with the page parameter
        api_url = f'http://localhost:8000/order/api/sale_order/{user_id}/{page}'
        api_response = requests.get(api_url)
        api_data = api_response.json()

        # Get the orders from the API response
        orders = api_data.get('orders', [])
        nested_page_range = api_data.get('page_range')

        # Flatten the nested lists
        int_page = int(page)
        # Flatten the nested lists
        page_range = list(chain.from_iterable(nested_page_range))

        if int_page + 1 <= int(page_range[-1]):
            print('yse')
            next_page = int_page + 1
        else:
            next_page = int_page
        if int_page - 1 >= int(page_range[0]):
            pre_page = int_page - 1
        else:
            pre_page = int_page

        return render(request, 'order/sale_order.html', {'orders': orders, 'user_id': user_id, 'page_range': page_range,"current_page": page, "next_page": next_page, "pre_page": pre_page})
    return HttpResponseNotAllowed(['GET'])
def want_order_detail(request, user_id, order_id):
    api_url = f'http://localhost:8000/order/api/want_order_detail/{user_id}/{order_id}'
    api_response = requests.get(api_url)
    api_response = api_response.json()
    books = api_response.get('books')
    poster_id = WantOrder.objects.get(orderid=order_id).userid

    if request.method == 'POST':
        for key, value in request.POST.items():
                if value == 'receive':
                    return redirect('order:receive', type='want_order', user_id=user_id,poster_id=poster_id, order_id=order_id)
    return render(request, 'order/detail/want_order_detail.html', {'books':books,'user_id': user_id, 'order_id': order_id})

def sale_order_detail(request, user_id, order_id):
    api_url = f'http://localhost:8000/order/api/sale_order_detail/{user_id}/{order_id}'
    api_response = requests.get(api_url)
    api_response = api_response.json()
    books = api_response.get('books')
    poster_id = SaleOrder.objects.get(orderid=order_id).userid.userid
    if request.method == 'POST':
        for key, value in request.POST.items():
                if value == 'receive':
                    return redirect('order:receive', type='sale_order', user_id=user_id , poster_id=poster_id, order_id=order_id)
    return render(request, 'order/detail/sale_order_detail.html', {'books':books,'user_id': user_id, 'order_id': order_id})

def receive(request, user_id, poster_id, order_id, type):
    api_url = f'http://localhost:8000/order/api/receive/{user_id}/{poster_id}/{order_id}/{type}'
    api_response = requests.post(api_url)
    print(api_response.content)
    api_response = api_response.json()
    poster = api_response.get('poster')
    return render(request, 'order/receive.html', {'type':type, 'user_id':user_id, 'poster': poster, 'order_id': order_id})