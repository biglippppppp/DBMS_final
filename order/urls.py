from django.urls import path
from . import views

app_name = 'order'
urlpatterns = [
    path('', views.index, name='index'),
    path('want_order/<int:user_id>', views.want_order, name='want_order'),
    path('sale_order/<int:user_id>', views.sale_order, name='sale_order'),
    path('want_order/<int:user_id>/detail/<int:order_id>', views.want_order_detail, name='want_order_detail'),
    path('sale_order/<int:user_id>/detail/<int:order_id>', views.sale_order_detail, name='sale_order_detail'),
    path('receive/<int:user_id>/<int:poster_id>/<int:order_id>/<str:type>', views.receive, name='receive'),
]