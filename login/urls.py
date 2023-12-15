from django.urls import path
from . import views
from .api_views import LoginAPIView
from .api_views import RegisterAPIView

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('api/login/', LoginAPIView.as_view(), name='login-api'),
    path('api/register/', RegisterAPIView.as_view(), name='register-api'),
]