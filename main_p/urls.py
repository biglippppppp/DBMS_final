from django.urls import path
from . import views
from .api_views import MainPAPIView
from .api_views import SearchAPIView
from .api_views import PostAPIView
from .views import new_create_order
from .views import create_sale_order
from .views import create_want_order

app_name = 'main_p'
urlpatterns = [
    path('<int:user_id>', views.index, name='index'),
    path('evaluate_user/<int:user_id>/', views.evaluate_user, name='evaluate_user'),
    path('search/<int:user_id>/', views.search, name='search'),
    path('search_result/<int:user_id>/', views.search_result, name='search_result'),
    path('new_create_order/<int:user_id>/', new_create_order, name='new_create_order'),
    path('create_saleOrder/<int:user_id>/', views.create_sale_order, name='create_saleOrder'),
    path('create_buyOrder/<int:user_id>/', views.create_want_order, name='create_buyOrder'),
    path('index/', views.self_info, name='self_info'),
    path('api/<int:user_id>/', MainPAPIView.as_view(), name='main-p-api'),
    path('api/search/<int:user_id>', SearchAPIView.as_view(), name='search-api'),
    path('api/posts/<int:user_id>/', PostAPIView.as_view(), name='post-api'),
    path('book_detail/<int:user_id>/<str:isbns>/', views.book_detail, name='book_detail'),
]