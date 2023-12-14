from django.urls import path
from . import views
from .api_views import SaleOrderAPIView
from .api_views import WantOrderAPIView
from .api_views import SaleOrderDetailAPIView
from .api_views import WantOrderDetailAPIView
from .api_views import ReceiveAPIView

app_name = 'order'
urlpatterns = [
    path('', views.index, name='index'),
    path('want_order/<int:user_id>', views.want_order, name='want_order'),
    path('sale_order/<int:user_id>', views.sale_order, name='sale_order'),
    path('want_order/<int:user_id>/detail/<int:order_id>', views.want_order_detail, name='want_order_detail'),
    path('sale_order/<int:user_id>/detail/<int:order_id>', views.sale_order_detail, name='sale_order_detail'),
    path('receive/<int:user_id>/<int:poster_id>/<int:order_id>/<str:type>', views.receive, name='receive'),
path('api/sale_order/<int:user_id>/', SaleOrderAPIView.as_view(), name='sale-order-api'),
    path('api/want_order/<int:user_id>/', WantOrderAPIView.as_view(), name='want-order-api'),
    path('api/sale_order_detail/<int:user_id>/<int:order_id>', SaleOrderDetailAPIView.as_view(),
         name='sale-order-detail-api'),
    path('api/want_order_detail/<int:user_id>/<int:order_id>', WantOrderDetailAPIView.as_view(), name='want-order-detail-api'),
    path('api/receive/<int:user_id>/<int:poster_id>/<int:order_id>/<str:type>', ReceiveAPIView.as_view(), name='receive-api'),
]