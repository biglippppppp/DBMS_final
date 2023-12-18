from django.shortcuts import render,redirect
import requests
from main_p.models import SaleOrder
from main_p.models import WantOrder
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class FakeUser:
        def __init__(self, user_id, user_name, role='user',email="p@gmail.com"):
            self.user_id = user_id
            self.user_name = user_name
            self.role = role
            self.email = email
class FakeBook:
        def __init__(self, isbn, price, description, receiver, status):
            self.isbn = isbn
            self.price = price
            self.description = description
            self.status = status
            self.receiver = receiver
            self.title = '假書名'
            self.author = '假作者'
class FakeOrder:
        def __init__(self, order_id, user_id, books):
            self.order_id = order_id
            self.user_id = user_id
            self.books = books
class FakeBook_detail:
        def __init__(self, isbn, price, description, poster, status):
            self.isbn = isbn
            self.price = price
            self.description = description
            self.poster = poster
            self.status = status
            self.title = '假書名'
            self.author = '假作者'
            self.category = ['理學院', "文學院"]
            self.courseID = '123456'
            self.academic_year = '112-1'
            self.courseName = '資料庫'
            self.teacherName = '孔子'





def index(request):
    return render(request, 'order/index.html')

def want_order(request, user_id):
    api_url = f'http://localhost:8000/order/api/want_order/{user_id}'
    api_response = requests.get(api_url)
    api_response = api_response.json()
    orders = api_response.get('orders')

    # 分頁
    items_per_page = 20
    paginator = Paginator(orders, items_per_page)
    page = request.GET.get('page')

    try:
        orders_page = paginator.page(page)
    except PageNotAnInteger:
        orders_page = paginator.page(1)
    except EmptyPage:
        orders_page = paginator.page(paginator.num_pages)

    return render(request, 'order/want_order.html', {'orders':orders_page,'user_id': user_id})

def sale_order(request, user_id):

    api_url = f'http://localhost:8000/order/api/sale_order/{user_id}'
    api_response = requests.get(api_url)
    api_response = api_response.json()
    orders = api_response.get('orders')

    # 分頁
    items_per_page = 20
    paginator = Paginator(orders, items_per_page)
    page = request.GET.get('page')

    try:
        orders_page = paginator.page(page)
    except PageNotAnInteger:
        orders_page = paginator.page(1)
    except EmptyPage:
        orders_page = paginator.page(paginator.num_pages)


    return render(request, 'order/sale_order.html', {'orders':orders_page,'user_id': user_id})

def want_order_detail(request, user_id, order_id):
    api_url = f'http://localhost:8000/order/api/sale_order_detail/{user_id}/{order_id}'
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