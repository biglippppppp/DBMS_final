from django.shortcuts import render,redirect
import requests
import json
app_name = 'self_info'
def index(request, user_id):
    api_url = f'http://localhost:8000/main_p/api/{user_id}'
    if request.method == 'POST':
        api_response = requests.post(api_url, data=request.POST)
        #改變html中按鈕的value可以達到按下不同按鈕後，跳轉到不同的頁面
        if request.POST.get('button') == 'personal_order':
            return redirect('self_info:personal_order', user_id=user_id)
    else:
        # Making a GET request to the API
        api_response = requests.get(api_url)

    api_data = api_response.json()
    user_info = api_data.get('user')
    return render(request, 'self_info/index.html', {'user_id': user_id, 'user_info': user_info})

def personal_order(request, user_id):
    if request.method == 'POST':
        #改變html中按鈕的value可以達到按下不同按鈕後，跳轉到不同的頁面
        if request.POST.get('button') == 'finished_order':
            return redirect('self_info:finish', user_id=user_id)
        if request.POST.get('button') == 'posting_order':
            return redirect('self_info:posting', user_id=user_id)
        if request.POST.get('button') == 'received_order':
            return redirect('self_info:received', user_id=user_id)
    return render(request, 'self_info/personal_order.html', {'user_id': user_id})

def finish(request, user_id):
    api_url = f'http://localhost:8000/self_info/api/finish/{user_id}'
    api_response = requests.get(api_url)
    api_response = api_response.json()
    orders = api_response.get('orders')
    want_orders = api_response.get('want_orders')
    return render(request, 'self_info/finish.html',  {'orders': orders,'user_id': user_id, 'want_orders': want_orders})

def posting(request, user_id):
    api_url = f'http://localhost:8000/self_info/api/posting/{user_id}'
    api_response = requests.get(api_url)
    api_response = api_response.json()
    orders = api_response.get('orders')
    want_orders = api_response.get('want_orders')
    return render(request, 'self_info/posting.html', {'orders': orders,'user_id': user_id, 'want_orders': want_orders})
def received(request, user_id):
    # 創建假用戶數據
    api_url = f'http://localhost:8000/self_info/api/receive/{user_id}'
    api_response = requests.get(api_url)
    api_response = api_response.json()
    orders = api_response.get('orders')
    want_orders = api_response.get('want_orders')
    return render(request, 'self_info/received.html', {'orders': orders,'user_id': user_id, 'want_orders': want_orders})

def finish_sell_detail(request, order_id, user_id):
    api_url = f'http://localhost:8000/self_info/api/finish_sell_detail/{user_id}/{order_id}'
    api_response = requests.get(api_url)
    api_response = api_response.json()
    books = api_response.get('books')
    
    if request.method == 'POST':
        for key, value in request.POST.items():
                if value == 'evaluate':
                    evaluated_user_id = int(key.split('_')[1])
                    return redirect('evaluate:evaluate_detail', user_id=evaluated_user_id)
    return render(request, 'self_info/detail/finish_sell_detail.html', {'books': books,'user_id': user_id, 'order_id': order_id})

def posting_sell_detail(request, order_id, user_id):
    api_url = f'http://localhost:8000/self_info/api/posting_sell_detail/{user_id}/{order_id}'
    api_response = requests.get(api_url)
    api_response = api_response.json()
    books = api_response.get('books')
    if request.method == 'POST':
        # 檢查每個按鈕
        for key, value in request.POST.items():
                if value == 'evaluate':
                    evaluated_user_id = int(key.split('_')[1])
                    return redirect('evaluate:evaluate_detail', user_id=evaluated_user_id)
                elif value == 'renew':
                    # 處理更新狀態的按鈕
                    # 從按鈕名稱中提取書籍的 isbn 和訂單 ID
                    parts = key.split('_')
                    renew_isbn = parts[1]
                    renew_order_id = int(parts[2])
                    renew_status = request.POST.get(f'status_{renew_isbn}')
                    data = {
                        'order_id': renew_order_id,
                        'isbn': renew_isbn,
                        'status': renew_status,
                        'type': 'sell',
                    }
                    url = f'http://localhost:8000/self_info/api/renew'
                    response = requests.post(url, json=data)

    return render(request, 'self_info/detail/posting_sell_detail.html', {'books': books,'user_id': user_id, 'order_id': order_id})

def received_sell_detail(request, order_id, user_id):
    api_url = f'http://localhost:8000/self_info/api/receive_sell_detail/{user_id}/{order_id}'
    api_response = requests.get(api_url)
    api_response = api_response.json()
    books = api_response.get('books')
    if request.method == 'POST':
        for key, value in request.POST.items():
                if value == 'evaluate':
                    evaluated_user_id = int(key.split('_')[1])
                    return redirect('evaluate:evaluate_detail', user_id=evaluated_user_id)
    return render(request, 'self_info/detail/received_sell_detail.html', {'books': books,'user_id': user_id, 'order_id': order_id})

def finish_want_detail(request, order_id, user_id):
    api_url = f'http://localhost:8000/self_info/api/finish_want_detail/{user_id}/{order_id}'
    api_response = requests.get(api_url)
    api_response = api_response.json()
    books = api_response.get('books')

    if request.method == 'POST':
        for key, value in request.POST.items():
                if value == 'evaluate':
                    evaluated_user_id = int(key.split('_')[1])
                    return redirect('evaluate:evaluate_detail', user_id=evaluated_user_id)
    return render(request, 'self_info/detail/finish_want_detail.html', {'books': books,'user_id': user_id, 'order_id': order_id})

def posting_want_detail(request, order_id, user_id):
    api_url = f'http://localhost:8000/self_info/api/posting_want_detail/{user_id}/{order_id}'
    api_response = requests.get(api_url)
    api_response = api_response.json()
    books = api_response.get('books')
    if request.method == 'POST':
        # 檢查每個按鈕
        for key, value in request.POST.items():
                if value == 'evaluate':
                    evaluated_user_id = int(key.split('_')[1])
                    return redirect('evaluate:evaluate_detail', user_id=evaluated_user_id)
                elif value == 'renew':
                    # 處理更新狀態的按鈕
                    # 從按鈕名稱中提取書籍的 isbn 和訂單 ID
                    parts = key.split('_')
                    renew_isbn = parts[1]
                    renew_order_id = int(parts[2])
                    renew_status = request.POST.get(f'status_{renew_isbn}')
                    data = {
                        'order_id': renew_order_id,
                        'isbn': renew_isbn,
                        'status': renew_status,
                        'type': 'want',
                    }
                    url = f'http://localhost:8000/self_info/api/renew'
                    response = requests.post(url, json=data)

    return render(request, 'self_info/detail/posting_want_detail.html', {'books': books,'user_id': user_id, 'order_id': order_id})

def received_want_detail(request, order_id, user_id):
    api_url = f'http://localhost:8000/self_info/api/receive_want_detail/{user_id}/{order_id}'
    api_response = requests.get(api_url)
    api_response = api_response.json()
    books = api_response.get('books')
    if request.method == 'POST':
        for key, value in request.POST.items():
                if value == 'evaluate':
                    print(key)
                    evaluated_user_id = int(key.split('_')[1])
                    return redirect('evaluate:evaluate_detail', user_id=evaluated_user_id)
    return render(request, 'self_info/detail/received_want_detail.html', {'books': books1,'user_id': user_id, 'order_id': order_id})
    
def evaluate_detail(request, user_id):
    # Your view logic here
    if request.method == 'POST':
        # Process form data and save to the database
        return render(request, 'evaluate/evaluate_detail.html', {'user_id': user_id})
    else:
        return render(request, 'evaluate/evaluate_detail.html', {'user_id': user_id})