from django.shortcuts import render,redirect


app_name = 'evaluate'
def evaluate_detail(request, user_id):

    return render(request, 'evaluate/evaluate_detail.html', {'user_id': user_id})

