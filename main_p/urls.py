from django.urls import path
from . import views
from .api_views import MainPAPIView
from .api_views import SearchAPIView
from .api_views import PostAPIView

app_name = 'main_p'
urlpatterns = [
    path('<int:user_id>', views.index, name='index'),
    path('api/<int:user_id>/', MainPAPIView.as_view(), name='main-p-api'),
    path('api/search/<int:user_id>/', SearchAPIView.as_view(), name='search-api'),
    path('api/posts/<int:user_id>/', PostAPIView.as_view(), name='post-api'),

]