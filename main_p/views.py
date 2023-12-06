from django.shortcuts import render,redirect

app_name = 'main_p'
def index(request, user_id):
    fake_user = {'user_id': user_id, 'user_name': 'Jerry', 'role': 'user'}
    #輸入假資訊讓網頁顯示
    if request.method == 'POST':
        #改變html中按鈕的value可以達到按下不同按鈕後，跳轉到不同的頁面
        if request.POST.get('button') == 'self_info':
            return redirect('self_info:index', user_id=fake_user['user_id'])
    return render(request, 'main_p/index.html', {'user_id': user_id})
