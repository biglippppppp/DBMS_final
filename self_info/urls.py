from django.urls import path
from . import views

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
]