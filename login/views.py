from django.shortcuts import render,redirect


def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        fake_user_id = 1
        # task1: 檢查 username 和 password 是否正確
        if role == 'user':
            return redirect('main_p:index', user_id=fake_user_id)
        elif role == 'admin':
            return redirect('/admin/')

    return render(request, 'login/index.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        # task2: 在資料庫中新增一筆使用者資料
        return redirect('/')  

    return render(request, 'login/register.html')

