from django.shortcuts import render,redirect
from django.http import HttpResponse

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
    
def create_order(request, user_id):
    if request.method == 'POST':
        # Process form data and save to the database
        return render(request, 'main_p/create_order.html', {'user_id': user_id})
    else:
        return render(request, 'main_p/create_order.html', {'user_id': user_id})

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
        