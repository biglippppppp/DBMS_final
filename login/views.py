import json
from django.shortcuts import render, redirect
import requests
from django.contrib import messages

def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        role = request.POST.get('role')


        # Assuming your API endpoint for login is something like this
        api_url = 'http://localhost:8000/api/login/'

        # Making a POST request to the API
        api_response = requests.post(api_url, data={'username': username, 'password': password, 'role': role, 'email': email})

        # Checking if the API request was successful (status code 200)
        if api_response.status_code == 200:
            # Extracting user_id from the API response
            api_data = json.loads(api_response.text)
            user_id = api_data.get('user_id')

            # Redirecting to the desired URL
            if role == 'user':
                return redirect('main_p:index', user_id=user_id)
            elif role == 'admin':
                return redirect('admin_page:index')

    return render(request, 'login/index.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        # task2: 在資料庫中新增一筆使用者資料
        # Assuming your API endpoint for login is something like this
        api_url = 'http://localhost:8000/api/register/'

        # Making a POST request to the API
        api_response = requests.post(api_url, data={'username': username, 'password': password,
                                                    'email': email, 'confirm_password': confirm_password})
        api_response = api_response.json()

        message = api_response.get('message', '')

        # Use Django's messages framework to store the message
        messages.success(request, message)

        return redirect('/')
    return render(request, 'login/register.html', )