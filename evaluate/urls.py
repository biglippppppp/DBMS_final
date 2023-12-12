from django.urls import path
from . import views

app_name = 'evaluate'
urlpatterns = [
    path('evaluate_detail/<int:user_id>', views.evaluate_detail, name='evaluate_detail'),
    path('evaluate_user/<int:user_id>', views.evaluate_buyers, name='evaluate_buyers'),
    path('evaluate_user/<int:user_id>', views.evaluate_sellers, name='evaluate_sellers'),
    path('evaluate_write/<str::target_user>', views.write_review, name='write_review'),
]