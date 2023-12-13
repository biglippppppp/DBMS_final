from django.urls import path
from . import views
from .api_views import FinishAPIView
from .api_views import FinishSellAPIView
from .api_views import FinishWantAPIView
from .api_views import PostingSellAPIView
from .api_views import PostingWantAPIView
from .api_views import PostingAPIView
from .api_views import ReceiveAPIView
from .api_views import ReceiveSellAPIView
from .api_views import ReceiveWantAPIView

app_name = 'self_info'
urlpatterns = [
    path('<int:user_id>/', views.index, name='index'),
    path('personal_order/<int:user_id>', views.personal_order, name='personal_order'),
    path('personal_order/finish/<int:user_id>', views.finish, name='finish'),
    path('personal_order/posting/<int:user_id>', views.posting, name='posting'),
    path('personal_order/received/<int:user_id>', views.received, name='received'),
    path('personal_order/finish/<int:user_id>/finish_sell_detail/<int:order_id>', views.finish_sell_detail, name='finish_sell_detail'),
    path('personal_order/finish/<int:user_id>/posting_sell_detail/<int:order_id>', views.posting_sell_detail, name='posting_sell_detail'),
    path('personal_order/finish/<int:user_id>/received_sell_detail/<int:order_id>', views.received_sell_detail, name='received_sell_detail'),
    path('personal_order/finish/<int:user_id>/finish_want_detail/<int:order_id>', views.finish_want_detail, name='finish_want_detail'),
    path('personal_order/finish/<int:user_id>/posting_want_detail/<int:order_id>', views.posting_want_detail, name='posting_want_detail'),
    path('personal_order/finish/<int:user_id>/received_want_detail/<int:order_id>', views.received_want_detail, name='received_want_detail'),
    path('api/finish/<int:user_id>/', FinishAPIView.as_view(), name='finish-api'),
    path('api/finish_sell_detail/<int:user_id>/<int:order_id>', FinishSellAPIView.as_view(), name='finish-sell-api'),
    path('api/finish_want_detail/<int:user_id>/<int:order_id>', FinishWantAPIView.as_view(), name='finish-want-api'),
    path('api/posting_sell_detail/<int:user_id>/<int:order_id>', PostingSellAPIView.as_view(), name='posting-sell-api'),
    path('api/posting_want_detail/<int:user_id>/<int:order_id>', PostingWantAPIView.as_view(), name='posting-want-api'),
    path('api/posting/<int:user_id>/', PostingAPIView.as_view(), name='posting-api'),
    path('api/receive/<int:user_id>/', ReceiveAPIView.as_view(), name='receive-api'),
    path('api/receive_sell_detail/<int:user_id>/<int:order_id>', ReceiveSellAPIView.as_view(), name='receive-sell-api'),
    path('api/receive_want_detail/<int:user_id>/<int:order_id>', ReceiveWantAPIView.as_view(), name='receive-want-api'),

]