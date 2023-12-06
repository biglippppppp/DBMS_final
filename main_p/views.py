from django.shortcuts import render

app_name = 'main_p'
def index(request):
    return render(request, 'main_p/index.html')
