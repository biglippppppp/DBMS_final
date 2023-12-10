from django.shortcuts import render,redirect
class FakeUser:
        def __init__(self, user_id, user_name, role='user'):
            self.user_id = user_id
            self.user_name = user_name
            self.role = role
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
        def __init__(self, isbn, price, description, receiver, status):
            self.isbn = isbn
            self.price = price
            self.description = description
            self.status = status
            self.receiver = receiver
            self.title = '假書名'
            self.author = '假作者'
            self.category = ['理學院', "文學院"]
            self.courseID = '123456'
            self.academic_year = '112-1'
            self.courseName = '資料庫'
            self.teacherName = '孔子'
            
app_name = 'self_info'
def index(request, user_id):
    if request.method == 'POST':
        #改變html中按鈕的value可以達到按下不同按鈕後，跳轉到不同的頁面
        if request.POST.get('button') == 'personal_order':
            return redirect('self_info:personal_order', user_id=user_id)
    return render(request, 'self_info/index.html', {'user_id': user_id})

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

    # 創建假用戶數據
    user1 = FakeUser(3, 'Jerry3')
    user2 = FakeUser(2, 'Tom')

    books1 = [FakeBook("ISBN1", "100", "Description 1",user1,'finished'), FakeBook("ISBN2", "150", "Description 2",user1,'finished')]
    books2 = [FakeBook("ISBN3", "200", "Description 3",user2,'finished')]
    books3 = [FakeBook("ISBN4", None, "Description 1",user1,'finished'), FakeBook("ISBN2", None, "Description 2",user1,'finished')]
    books4 = [FakeBook("ISBN5", None, "Description 3",user2,'finished')]
    # 創建假訂單數據
    orders = [
        FakeOrder(1, user_id, books1),
        FakeOrder(2, user_id, books2),
        FakeOrder(3, user_id, books1),
        FakeOrder(4, user_id, books2),
        FakeOrder(5, user_id, books1),
        FakeOrder(6, user_id, books2),
    ]
    want_orders = [FakeOrder(7, user_id, books3), FakeOrder(8, user_id, books4),]
    return render(request, 'self_info/finish.html',  {'orders': orders,'user_id': user_id, 'want_orders': want_orders})

def posting(request, user_id):
    user1 = FakeUser(3, 'Jerry3')
    books1 = [FakeBook("ISBN1", "100", "Description 1",None,'posting'), FakeBook("ISBN2", "150", "Description 2",user1,'posting')]
    books2 = [FakeBook("ISBN3", "200", "Description 3",None,'posting')]
    books3 = [FakeBook("ISBN4", None, "Description 1",None,'posting'), FakeBook("ISBN2", None, "Description 2",user1,'posting')]
    books4 = [FakeBook("ISBN5", None, "Description 3",None,'posting')]
    # 創建假訂單數據
    orders = [
        FakeOrder(1, user_id, books1),
        FakeOrder(2, user_id, books2),
        FakeOrder(3, user_id, books1),
        FakeOrder(4, user_id, books2),
        FakeOrder(5, user_id, books1),
        FakeOrder(6, user_id, books2),
    ]
    want_orders = [FakeOrder(7, user_id, books3), FakeOrder(8, user_id, books4),]
    return render(request, 'self_info/posting.html', {'orders': orders,'user_id': user_id, 'want_orders': want_orders})
def received(request, user_id):
    # 創建假用戶數據
    user1 = FakeUser(3, 'Jerry3')
    user2 = FakeUser(2, 'Tom')

    books1 = [FakeBook("ISBN1", "100", "Description 1",user1,'finished'), FakeBook("ISBN2", "150", "Description 2",user1,'finished')]
    books2 = [FakeBook("ISBN3", "200", "Description 3",user2,'finished')]
    books3 = [FakeBook("ISBN4", None, "Description 1",user1,'finished'), FakeBook("ISBN2", None, "Description 2",user1,'finished')]
    books4 = [FakeBook("ISBN5", None, "Description 3",user2,'finished')]
    # 創建假訂單數據
    orders = [
        FakeOrder(1, user_id, books1),
        FakeOrder(2, user_id, books2),
        FakeOrder(3, user_id, books1),
        FakeOrder(4, user_id, books2),
        FakeOrder(5, user_id, books1),
        FakeOrder(6, user_id, books2),
    ]
    want_orders = [FakeOrder(7, user_id, books3), FakeOrder(8, user_id, books4),]
    return render(request, 'self_info/received.html', {'orders': orders,'user_id': user_id, 'want_orders': want_orders})

def finish_sell_detail(request, order_id, user_id):
    user1 = FakeUser(3, 'Jerry3')
    books1 = [FakeBook_detail("ISBN1", "100", "Description 1",user1,'finished'), FakeBook_detail("ISBN2", "150", "Description 2",user1,'finished')]
    
    if request.method == 'POST':
        for key, value in request.POST.items():
                if value == 'evaluate':
                    evaluated_user_id = int(key.split('_')[1])
                    return redirect('evaluate:evaluate_detail', user_id=evaluated_user_id)
    return render(request, 'self_info/detail/finish_sell_detail.html', {'books': books1,'user_id': user_id, 'order_id': order_id})

def posting_sell_detail(request, order_id, user_id):
    user1 = FakeUser(3, 'Jerry3')
    books1 = [FakeBook_detail("ISBN1", "100", "Description 1",None,'posting'), FakeBook_detail("ISBN2", "150", "Description 2",user1,'posting')]
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

    return render(request, 'self_info/detail/posting_sell_detail.html', {'books': books1,'user_id': user_id, 'order_id': order_id})

def received_sell_detail(request, order_id, user_id):
    user1 = FakeUser(3, 'Jerry3')
    books1 = [FakeBook_detail("ISBN1", "100", "Description 1",user1,'finished'), FakeBook_detail("ISBN2", "150", "Description 2",user1,'finished')]
    
    if request.method == 'POST':
        for key, value in request.POST.items():
                if value == 'evaluate':
                    evaluated_user_id = int(key.split('_')[1])
                    return redirect('evaluate:evaluate_detail', user_id=evaluated_user_id)
    return render(request, 'self_info/detail/received_sell_detail.html', {'books': books1,'user_id': user_id, 'order_id': order_id})

def finish_want_detail(request, order_id, user_id):
    user1 = FakeUser(3, 'Jerry3')
    books1 = [FakeBook_detail("ISBN1", None, "Description 1",user1,'finished'), FakeBook_detail("ISBN2", None, "Description 2",user1,'finished')]
    
    if request.method == 'POST':
        for key, value in request.POST.items():
                if value == 'evaluate':
                    evaluated_user_id = int(key.split('_')[1])
                    return redirect('evaluate:evaluate_detail', user_id=evaluated_user_id)
    return render(request, 'self_info/detail/finish_want_detail.html', {'books': books1,'user_id': user_id, 'order_id': order_id})

def posting_want_detail(request, order_id, user_id):
    user1 = FakeUser(3, 'Jerry3')
    books1 = [FakeBook_detail("ISBN1", None, "Description 1",None,'posting'), FakeBook_detail("ISBN2", None, "Description 2",user1,'posting')]
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

    return render(request, 'self_info/detail/posting_want_detail.html', {'books': books1,'user_id': user_id, 'order_id': order_id})

def received_want_detail(request, order_id, user_id):
    user1 = FakeUser(3, 'Jerry3')
    books1 = [FakeBook_detail("ISBN1", None, "Description 1",user1,'finished'), FakeBook_detail("ISBN2", None, "Description 2",user1,'finished')]
    if request.method == 'POST':
        for key, value in request.POST.items():
                if value == 'evaluate':
                    print(key)
                    evaluated_user_id = int(key.split('_')[1])
                    return redirect('evaluate:evaluate_detail', user_id=evaluated_user_id)
    return render(request, 'self_info/detail/received_want_detail.html', {'books': books1,'user_id': user_id, 'order_id': order_id})