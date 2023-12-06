from django.shortcuts import render,redirect


app_name = 'self_info'
def index(request, user_id):
    if request.method == 'POST':
        #改變html中按鈕的value可以達到按下不同按鈕後，跳轉到不同的頁面
        if request.POST.get('button') == 'personal_order':
            return redirect('self_info:personal_order', user_id=user_id)
    return render(request, 'self_info/index.html', {'user_id': user_id})

def personal_order(request, user_id):
    # if request.method == 'POST':
    #     #改變html中按鈕的value可以達到按下不同按鈕後，跳轉到不同的頁面
    #     if request.POST.get('button') == 'personal_order':
    #         return redirect('self_info:personal_order', user_id=user_id)
    return render(request, 'self_info/personal_order.html', {'user_id': user_id})
