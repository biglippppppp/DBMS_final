from django.urls import path
from . import views

app_name = 'evaluate'
urlpatterns = [
    path('evaluate_detail/<int:user_id>', views.evaluate_detail, name='evaluate_detail'),
]