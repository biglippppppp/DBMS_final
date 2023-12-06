from django.urls import path
from . import views

app_name = 'self_info'
urlpatterns = [
    path('<int:user_id>/', views.index, name='index'),
    path('personal_order/<int:user_id>', views.personal_order, name='personal_order'),
]