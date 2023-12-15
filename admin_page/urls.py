from django.urls import path
from . import views

app_name = 'admin_page'
urlpatterns = [
    path('', views.index, name='index'),
    path('select/', views.select, name='select'),
    path('insert/', views.insert, name='insert'),
    path('delete/', views.delete, name='delete'),
    path('update/', views.update, name='update'),
    path('output/', views.output, name='output'),
]