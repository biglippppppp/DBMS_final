from django.urls import path
from . import views

app_name = 'evaluate'
urlpatterns = [
    path('evaluate_detail/<int:user_id>', views.evaluate_detail, name='evaluate_detail'),
    path('evaluate_user/<int:user_id>/', views.evaluate_user, name='evaluate_user'),
    path('evaluate_write/<int:user_id>', views.write_review, name='write_review'),
]