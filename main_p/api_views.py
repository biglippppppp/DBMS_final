from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from main_p.models import Users
from main_p.models import Book
from main_p.models import BookCategory
from main_p.models import UserRole
from .models import SaleOrder
from .models import WantOrder
from .models import Sell
from .models import LookFor
from django.utils import timezone
from self_info.models import Order
from self_info.api_views import OrderSerializer
from self_info.models import Book_object
from self_info.api_views import BookObjectSerializer
from self_info.api_views import UserSerializer
from self_info.models import User
from .models import ReceiveWant
from .models import ReceiveSale
from django.core.paginator import Paginator
from django.db.models import Q
from evaluate.api_views import UsersSerializer


class MainPAPIView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        user = Users.objects.get(userid=user_id)
        username = user.username
        serializer = UsersSerializer(user)

        return Response({'message': f'API for user {user_id}', 'username': username, 'user': serializer.data})


class PostAPIView(APIView):
    def post(self, request, user_id, *args, **kwargs):
        user = Users.objects.get(userid=user_id)
        order_type = request.data.get('order_type')

        if order_type == 'sell':
            book_counter = 1
            order_id = SaleOrder.objects.count() + 1
            current_datetime = timezone.now()
            current_date = current_datetime.date()
            sale_order = SaleOrder.objects.create(orderid=order_id, userid=user, postdate=current_date)

            while True:
                isbn_key = f'isbn_{book_counter}'
                price_key = f'price_{book_counter}'
                description_key = f'description_{book_counter}'

                isbn = request.data.get(isbn_key)
                price = request.data.get(price_key)
                description = request.data.get(description_key)
                status = 'Posting'

                if isbn is None:
                    # No more books, break out of the loop
                    break


                book = Book.objects.get(isbn=isbn)
                Sell.objects.create(orderid=sale_order, isbn=book, price=price, status=status, description=description, finishdate=None)
                book_counter += 1



        else:
            book_counter = 1
            order_id = WantOrder.objects.count() + 1
            current_datetime = timezone.now()
            current_date = current_datetime.date()
            want_order = WantOrder.objects.create(orderid=order_id, userid=user, postdate=current_date)

            while True:
                isbn_key = f'isbn_{book_counter}'
                description_key = f'description_{book_counter}'

                isbn = request.data.get(isbn_key)
                description = request.data.get(description_key)
                status = 'Posting'

                if isbn is None:
                    # No more books, break out of the loop
                    break

                book = Book.objects.get(isbn=isbn)

                LookFor.objects.create(orderid=want_order, isbn=book, status=status, description=description, finishdate=None)
                book_counter += 1



        return Response({'user_id': user_id, 'order_id': order_id})


class SearchAPIView(APIView):
    def post(self, request, *args, **kwargs):
        orders = []
        order_type = request.data.get('order_type')
        category = request.data.get('category')
        key_word = request.data.get('keyword')

        current_order_id = 0
        while len(orders) < 100:
            sale_orders = SaleOrder.objects.filter(orderid__gt=current_order_id)[:100]
            if not sale_orders:
                break

            for sale_order in sale_orders:
                sells = Sell.objects.filter(orderid=sale_order.orderid)
                books = []

                for sell in sells:
                    category_bool = False
                    isbn = sell.isbn.isbn
                    price = sell.price
                    status = sell.status
                    book_categories = BookCategory.objects.filter(isbn=isbn)

                    for book_category in book_categories:
                        if book_category.category == category:
                            category_bool = True

                    if key_word is None:
                        if status == 'Posting' and category_bool:
                            description = sell.description
                            try:
                                receive_sale = ReceiveSale.objects.get(orderid=sale_order.orderid)
                                receiverid = receive_sale.userid.userid
                                receivername = Users.objects.get(userid=receiverid).username
                                receiver = User(receiverid, receivername)
                            except ReceiveSale.DoesNotExist:
                                receiver = User(0, "不存在")

                            book = Book.objects.get(isbn=isbn)
                            title = book.title
                            author = book.author
                            new_book = Book_object(isbn, price, description, receiver, status, title, author)
                            books.append(new_book)
                    else:
                        book = Book.objects.get(isbn=isbn)
                        title = book.title
                        author = book.author

                        if status == 'Posting' and category_bool and (
                                key_word.lower() in title.lower() or key_word.lower() in author.lower()):
                            description = sell.description
                            try:
                                receive_sale = ReceiveSale.objects.get(orderid=sale_order.orderid)
                                receiverid = receive_sale.userid.userid
                                receivername = Users.objects.get(userid=receiverid).username
                                receiver = User(receiverid, receivername)
                            except ReceiveSale.DoesNotExist:
                                receiver = User(0, "不存在")

                            new_book = Book_object(isbn, price, description, receiver, status, title, author)
                            books.append(new_book)

                if books:
                    new_order = Order(sale_order.orderid, user_id, books)
                    orders.append(new_order)
            current_order_id = current_order_id + 100

        orders_serializer = OrderSerializer(orders, many=True)
        return Response({'orders': orders_serializer.data, 'user_id': user_id})