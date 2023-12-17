from django.shortcuts import render,redirect
from django.http import HttpResponse
import requests
import json

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
    return render(request, 'main_p/index.html', {'user_id': user_id, 'user_info': user_info})
    
def create_order(request, user_id):
    if request.method == 'POST':
        if request.POST.get('button') == 'submit':
            api_url = f'http://localhost:8000/main_p/api/posts/{user_id}/'
            order_type = request.POST.get('order_type')
            # Process form data and save to the database
            if order_type == 'sell':
                book_counter = 1
                form_data = {
                    'order_type': order_type,
                }

                while True:
                    isbn_key = f'isbn_{book_counter}'
                    price_key = f'price_{book_counter}'
                    description_key = f'description_{book_counter}'

                    isbn = request.POST.get(isbn_key)

                    if isbn is None:
                        # No more books, break out of the loop
                        break

                    # Collect data for the current book
                    form_data[f'isbn_{book_counter}'] = isbn
                    form_data[f'price_{book_counter}'] = request.POST.get(price_key)
                    form_data[f'description_{book_counter}'] = request.POST.get(description_key)

                    book_counter += 1

                # Make a single API request after the loop
                api_response = requests.post(api_url, data=form_data)
                api_response = api_response.json()
                order_id = api_response.get('order_id')
                return redirect('self_info:posting_sell_detail', user_id=user_id, order_id=order_id)

            else:
                book_counter = 1
                form_data = {
                    'order_type': order_type,
                }

                while True:
                    isbn_key = f'isbn_{book_counter}'
                    description_key = f'description_{book_counter}'

                    isbn = request.POST.get(isbn_key)

                    if isbn is None:
                        # No more books, break out of the loop
                        break

                    # Collect data for the current book
                    form_data[f'isbn_{book_counter}'] = isbn
                    form_data[f'description_{book_counter}'] = request.POST.get(description_key)

                    book_counter += 1

                # Make a single API request after the loop
                api_response = requests.post(api_url, data=form_data)
                api_response = api_response.json()
                order_id = api_response.get('order_id')
                return redirect('self_info:posting_want_detail', user_id=user_id, order_id=order_id)

    return render(request, 'main_p/create_order.html', {'user_id':user_id})

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
