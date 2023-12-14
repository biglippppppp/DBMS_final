from django.shortcuts import render,redirect
import pandas as pd

app_name = 'admin_page'
def index(request):
    if request.method == 'POST':
        #改變html中按鈕的value可以達到按下不同按鈕後，跳轉到不同的頁面
        if request.POST.get('button') == 'select':
            return redirect('admin_page:select')
        elif request.POST.get('button') == 'insert':
            return redirect('admin_page:insert')
        elif request.POST.get('button') == 'delete':
            return redirect('admin_page:delete')
        elif request.POST.get('button') == 'update':
            return redirect('admin_page:update')
    return render(request, 'admin_page/index.html')

def select(request):
    if request.method == 'POST':
        # 從 POST 請求中獲取數據
        if request.POST.get('button') == 'admin_page':
            return redirect('admin_page:index')
        select_content = request.POST.get('select_content')
        selected_table = request.POST.get('table')
        sql_content = request.POST.get('sql')
        if sql_content == '':
            sql_sentence = 'SELECT ' + select_content + ' FROM ' + selected_table
        else:
            sql_sentence = 'SELECT ' + select_content + ' FROM ' + selected_table + " " + sql_content
        print(sql_sentence)
        try:
            #與資料庫連線
            fake_output = {'user_id': ['1','2'], 'user_name': ['Jerry', 'berry'], 'role': ['user', 'user']}
            output = fake_output
            type = 'select'
        except:
            output = 'failed connect to database'
            type = 'not_select'
        request.session['output'] = output
        request.session['type'] = type
        return redirect('admin_page:output')
    return render(request, 'admin_page/select.html')

def insert(request):
    if request.method == 'POST':
        if request.POST.get('button') == 'admin_page':
            return redirect('admin_page:index')
        # 從 POST 請求中獲取數據

        selected_table = request.POST.get('table')
        sql_content = request.POST.get('sql')
        sql_sentence = 'INSERT INTO ' + selected_table + ' VALUES (' + sql_content + ')'
        print(sql_sentence)
        try:
            #與資料庫連線
            output = 'request success'
        except:
            output = 'failed connect to database'
        request.session['output'] = output
        request.session['type'] = 'not_select'
        return redirect('admin_page:output')

    return render(request, 'admin_page/insert.html')

def delete(request):
    if request.method == 'POST':
        if request.POST.get('button') == 'admin_page':
            return redirect('admin_page:index')
        # 從 POST 請求中獲取數據
        selected_table = request.POST.get('table')
        where_content = request.POST.get('sql')
        sql_sentence = 'DELETE FROM ' + selected_table + ' WHERE ' + where_content
        print(sql_sentence)
        try:
            #與資料庫連線
            output = 'request success'
        except:
            output = 'failed connect to database'
        request.session['output'] = output
        request.session['type'] = 'not_select'
        return redirect('admin_page:output')
    return render(request, 'admin_page/delete.html')

def update(request):
    if request.method == 'POST':
        if request.POST.get('button') == 'admin_page':
            return redirect('admin_page:index')
        if request.POST.get('button') == 'send':
            # 從 POST 請求中獲取數據
            selected_table = request.POST.get('table')
            set_content = request.POST.get('set')
            where_content = request.POST.get('sql')
            sql_sentence = 'UPDATE ' + selected_table + ' SET ' + set_content + ' WHERE ' + where_content
            print(sql_sentence)
            try:
                #與資料庫連線
                output = 'request success'
            except:
                output = 'failed connect to database'
            request.session['output'] = output
            request.session['type'] = 'not_select'
            return redirect('admin_page:output')
    return render(request, 'admin_page/update.html')

def output(request):
    output = request.session['output']
    type = request.session['type']
    if request.method == 'POST':
        # 從 POST 請求中獲取數據
        if request.POST.get('button') == 'admin_page':
            return redirect('admin_page:index')
    if type != 'not_select':
        output = pd.DataFrame(output)
        html_table = output.to_html(classes='table')
        return render(request, 'admin_page/output.html', {'output':html_table,'type': type})
    return render(request, 'admin_page/output.html', {'output':output,'type': type})