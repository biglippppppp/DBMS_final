from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from main_p.models import Users
from main_p.models import UserRole
from main_p.models import Book
from main_p.models import BookCategory
from main_p.models import Course
from main_p.models import LookFor
from main_p.models import ReceiveSale
from main_p.models import ReceiveWant
from main_p.models import Require
from main_p.models import SaleOrder
from main_p.models import Sell
from main_p.models import WantOrder
from .models import Book_object
from .models import Book_detail
from .models import Order
from .models import User
from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
from evaluate.api_views import UsersSerializer
from order.api_views import BookSimpleSerializer




class UserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    user_name = serializers.CharField()

    def create(self, validated_data):
        # Create and return a new User instance using the validated data
        return User(**validated_data)


class BookDetailSerializer(serializers.Serializer):
    isbn = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField()
    status = serializers.CharField()
    receiver = UserSerializer()
    title = serializers.CharField()
    author = serializers.CharField()
    category = serializers.CharField()
    courseID = serializers.CharField()
    academic_year = serializers.CharField()
    course_name = serializers.CharField(source='courseName')  # Map to the correct attribute
    teacher_name = serializers.CharField(source='teacherName')  # Map to the correct attribute
    def to_representation(self, instance):
        # Override the to_representation method to handle custom serialization
        representation = super().to_representation(instance)
        # Add any additional custom serialization logic here
        return representation


class BookObjectSerializer(serializers.Serializer):
    isbn = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField()
    receiver = UserSerializer()
    status = serializers.CharField()
    title = serializers.CharField()
    author = serializers.CharField()

    def create(self, validated_data):
        # Create and return a new Book_object instance using the validated data
        return Book_object(**validated_data)



class OrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    books = BookSimpleSerializer(many=True)

    def create(self, validated_data):
        # Create and return a new Order instance using the validated data
        return Order(**validated_data)



class FinishAPIView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        sale_orders_list = []
        want_orders_list = []

        sale_orders = SaleOrder.objects.filter(userid=user_id)
        for order in sale_orders:
            sells = Sell.objects.filter(orderid=order.orderid)
            books = []
            posting_bool = False
            for sell in sells:
                if sell.status == 'Posting':
                    posting_bool = True
            if not posting_bool:
                for sell in sells:
                    isbn = sell.isbn.isbn
                    price = sell.price
                    book = Book.objects.get(isbn=isbn)
                    title = book.title
                    new_book = BookSimpleSerializer({'isbn': isbn, 'price': price, 'title': title}).data
                    books.append(new_book)
                if books != []:
                    fakeorder = Order(order.orderid, user_id, books)
                    sale_orders_list.append(fakeorder)

        want_orders = []
        wo = WantOrder.objects.filter(userid=user_id)
        for order in wo:
            posting_bool = False
            sells = LookFor.objects.filter(orderid=order.orderid)
            books = []

            for sell in sells:
                if sell.status == 'Posting':
                    posting_bool = True
            if not posting_bool:
                for sell in sells:
                    isbn = sell.isbn.isbn
                    price = None
                    book = Book.objects.get(isbn=isbn)
                    title = book.title
                    new_book = BookSimpleSerializer({'isbn': isbn, 'price': price, 'title': title}).data
                    books.append(new_book)
                if books != []:
                    fakeorder = Order(order.orderid, user_id, books)
                    want_orders_list.append(fakeorder)

        sale_orders_serializer = OrderSerializer(sale_orders_list, many=True)
        want_orders_serializer = OrderSerializer(want_orders_list, many=True)

        return Response({
            'orders': sale_orders_serializer.data,
            'user_id': user_id,
            'want_orders': want_orders_serializer.data
        })


class PostingAPIView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        sale_orders_list = []
        want_orders_list = []

        sale_orders = SaleOrder.objects.filter(userid=user_id)
        for order in sale_orders:
            sells = Sell.objects.filter(orderid=order.orderid)
            books = []
            posting_bool = False
            for sell in sells:
                if sell.status == 'Posting':
                    posting_bool = True
            if posting_bool:
                for sell in sells:
                    isbn = sell.isbn.isbn
                    price = sell.price
                    book = Book.objects.get(isbn=isbn)
                    title = book.title
                    new_book = BookSimpleSerializer({'isbn': isbn, 'price': price, 'title': title}).data
                    books.append(new_book)

                if books != []:
                    fakeorder = Order(order.orderid, user_id, books)
                    sale_orders_list.append(fakeorder)

        want_orders = []
        wo = WantOrder.objects.filter(userid=user_id)
        for order in wo:
            sells = LookFor.objects.filter(orderid=order.orderid)
            books = []
            posting_bool = False
            for sell in sells:
                if sell.status == 'Posting':
                    posting_bool = True
            print('fwjifcmdcii', posting_bool, order.orderid)
            if posting_bool:
                for sell in sells:
                    isbn = sell.isbn.isbn
                    price = None
                    book = Book.objects.get(isbn=isbn)
                    title = book.title
                    new_book = BookSimpleSerializer({'isbn': isbn, 'price': price, 'title': title}).data
                    books.append(new_book)
                if books != []:
                    fakeorder = Order(order.orderid, user_id, books)
                    want_orders_list.append(fakeorder)

        sale_orders_serializer = OrderSerializer(sale_orders_list, many=True)
        want_orders_serializer = OrderSerializer(want_orders_list, many=True)

        return Response({
            'orders': sale_orders_serializer.data,
            'user_id': user_id,
            'want_orders': want_orders_serializer.data
        })


class FinishSellAPIView(APIView):
    def get(self, request, user_id, order_id, *args, **kwargs):
        receiver_ids = []
        users = []
        receive_sales = ReceiveSale.objects.filter(orderid=order_id)
        for receive_sale in receive_sales:
            receiver_ids.append(receive_sale.userid.userid)
        for id in receiver_ids:
            users.append(Users.objects.get(userid=id))
        user_serializer = UsersSerializer(users, many=True)
        books_details = []
        sells = Sell.objects.filter(orderid=order_id)
        for sell in sells:
            isbn = sell.isbn.isbn
            price = sell.price
            description = sell.description
            status = sell.status
            book = Book.objects.get(isbn=isbn)
            title = book.title
            author = book.author
            requires = Require.objects.filter(isbn=isbn)
            for require in requires:
                course_id = require.courseid.courseid
                course = Course.objects.get(courseid=course_id)
                academic_year = course.academicyear
            book_categories = BookCategory.objects.filter(isbn=isbn)
            for book_category in book_categories:
                category = book_category.category
            courseName = course.coursename
            teacherName = course.instructorname
            book_detail = {
                'isbn': isbn,
                'price': price,
                'description': description,
                'receiver': None,
                'status': status,
                'title': title,
                'author':author,
                'category':category,
                'courseID': course_id,
                'academic_year': academic_year,
                'courseName': courseName,
                'teacherName': teacherName,
            }

            books_details.append(book_detail)

        serializer = BookDetailSerializer(data=books_details, many=True)
        serializer.is_valid()

        # Serialize the data
        serialized_data = serializer.data

        return Response({'books': serialized_data, 'user_id': user_id, 'order_id': order_id, 'receivers': user_serializer.data})

class FinishWantAPIView(APIView):
    def get(self, request, user_id, order_id, *args, **kwargs):
        receiver_ids = []
        users = []
        receive_sales = ReceiveWant.objects.filter(orderid=order_id)
        for receive_sale in receive_sales:
            receiver_ids.append(receive_sale.userid.userid)
        for id in receiver_ids:
            users.append(Users.objects.get(userid=id))
        user_serializer = UsersSerializer(users, many=True)
        books_details = []
        sells = LookFor.objects.filter(orderid=order_id)
        for sell in sells:
            isbn = sell.isbn.isbn
            status = sell.status
            description = sell.description
            receiver = None
            book = Book.objects.get(isbn=isbn)
            title = book.title
            author = book.author
            requires = Require.objects.filter(isbn=isbn)
            for require in requires:
                course_id = require.courseid.courseid
                course = Course.objects.get(courseid=course_id)
                academic_year = course.academicyear
            book_categories = BookCategory.objects.filter(isbn=isbn)
            for book_category in book_categories:
                category = book_category.category
            courseName = course.coursename
            teacherName = course.instructorname
            book_detail = {
                'isbn': isbn,
                'price': None,
                'description': description,
                'receiver': receiver,
                'status': status,
                'title': title,
                'author': author,
                'category': category,
                'courseID': course_id,
                'academic_year': academic_year,
                'courseName': courseName,
                'teacherName': teacherName,
            }
            books_details.append(book_detail)

        serializer = BookDetailSerializer(data=books_details, many=True)
        serializer.is_valid()

        # Serialize the data
        serialized_data = serializer.data

        return Response({'books': serialized_data, 'user_id': user_id, 'order_id': order_id, 'receivers': user_serializer.data})


class PostingSellAPIView(APIView):
    def get(self, request, user_id, order_id, *args, **kwargs):
        receiver_ids = []
        users = []
        receive_sales = ReceiveSale.objects.filter(orderid=order_id)
        for receive_sale in receive_sales:
            receiver_ids.append(receive_sale.userid.userid)
        for id in receiver_ids:
            users.append(Users.objects.get(userid=id))
        user_serializer = UsersSerializer(users, many=True)
        books_details = []
        sells = Sell.objects.filter(orderid=order_id)
        for sell in sells:
            isbn = sell.isbn.isbn
            price = sell.price
            description = sell.description
            status = sell.status
            receiver = None
            book = Book.objects.get(isbn=isbn)
            title = book.title
            author = book.author
            requires = Require.objects.filter(isbn=isbn)
            for require in requires:
                course_id = require.courseid.courseid
                course = Course.objects.get(courseid=course_id)
                academic_year = course.academicyear
            book_categories = BookCategory.objects.filter(isbn=isbn)
            for book_category in book_categories:
                category = book_category.category
            courseName = course.coursename
            teacherName = course.instructorname
            book_detail = {
                'isbn': isbn,
                'price': price,
                'description': description,
                'receiver': receiver,
                'status': status,
                'title': title,
                'author': author,
                'category': category,
                'courseID': course_id,
                'academic_year': academic_year,
                'courseName': courseName,
                'teacherName': teacherName,
            }
            books_details.append(book_detail)

        serializer = BookDetailSerializer(data=books_details, many=True)
        serializer.is_valid()

        # Serialize the data
        serialized_data = serializer.data

        return Response({'books': serialized_data, 'user_id': user_id, 'order_id': order_id, 'receivers': user_serializer.data})

class PostingWantAPIView(APIView):
    def get(self, request, user_id, order_id, *args, **kwargs):
        receiver_ids = []
        users = []
        receive_sales = ReceiveWant.objects.filter(orderid=order_id)
        for receive_sale in receive_sales:
            receiver_ids.append(receive_sale.userid.userid)
        for id in receiver_ids:
            users.append(Users.objects.get(userid=id))
        user_serializer = UsersSerializer(users, many=True)
        books_details = []
        sells = LookFor.objects.filter(orderid=order_id)
        for sell in sells:
            isbn = sell.isbn.isbn
            status = sell.status
            description = sell.description
            receiver = User(0, '不存在')
            book = Book.objects.get(isbn=isbn)
            title = book.title
            author = book.author
            requires = Require.objects.filter(isbn=isbn)
            for require in requires:
                course_id = require.courseid.courseid
                course = Course.objects.get(courseid=course_id)
                academic_year = course.academicyear
            book_categories = BookCategory.objects.filter(isbn=isbn)
            for book_category in book_categories:
                category = book_category.category
            courseName = course.coursename
            teacherName = course.instructorname
            book_detail = {
                'isbn': isbn,
                'price': None,
                'description': description,
                'receiver': receiver,
                'status': status,
                'title': title,
                'author': author,
                'category': category,
                'courseID': course_id,
                'academic_year': academic_year,
                'courseName': courseName,
                'teacherName': teacherName,
            }

            books_details.append(book_detail)

        serializer = BookDetailSerializer(data=books_details, many=True)
        serializer.is_valid()

        # Serialize the data
        serialized_data = serializer.data

        return Response({'books': serialized_data, 'user_id': user_id, 'order_id': order_id, 'receivers': user_serializer.data})

class ReceiveAPIView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        sale_orders_receive = []
        want_orders_receive = []

        receives = ReceiveSale.objects.filter(userid=user_id)

        for receive in receives:
            books = []
            sells = Sell.objects.filter(orderid=receive.orderid.orderid)
            for sell in sells:
                isbn = sell.isbn.isbn
                price = sell.price
                description = sell.description
                status = sell.status
                sale_order = SaleOrder.objects.get(orderid=receive.orderid.orderid)
                poster_id = sale_order.userid.userid
                poster_name = Users.objects.get(userid=poster_id).username
                poster = User(poster_id, poster_name)
                book = Book.objects.get(isbn=isbn)
                title = book.title
                author = book.author
                new_book = Book_object(isbn, price, description, poster, status, title, author)
                books.append(new_book)

            if books != []:
                fakeorder = Order(receive.orderid.orderid, user_id, books)
                sale_orders_receive.append(fakeorder)

        receives = ReceiveWant.objects.filter(userid=user_id)

        for receive in receives:
            books = []
            sells = LookFor.objects.filter(orderid=receive.orderid.orderid)
            for sell in sells:
                isbn = sell.isbn.isbn
                status = sell.status
                sale_order = WantOrder.objects.get(orderid=receive.orderid.orderid)
                poster_id = sale_order.userid.userid
                poster_name = Users.objects.get(userid=poster_id).username
                poster = User(poster_id, poster_name)
                book = Book.objects.get(isbn=isbn)
                title = book.title
                author = book.author
                new_book = Book_object(isbn, None, None, poster, status, title, author)
                books.append(new_book)

            if books != []:
                fakeorder = Order(receive.orderid.orderid, user_id, books)
                sale_orders_receive.append(fakeorder)

        sale_orders_serializer = OrderSerializer(sale_orders_receive, many=True)
        want_orders_serializer = OrderSerializer(want_orders_receive, many=True)

        return Response({
            'orders': sale_orders_serializer.data,
            'user_id': user_id,
            'want_orders': want_orders_serializer.data
        })

class ReceiveSellAPIView(APIView):
    def get(self, request, user_id, order_id, *args, **kwargs):
        books_details = []
        sells = Sell.objects.filter(orderid=order_id)
        for sell in sells:
            isbn = sell.isbn.isbn
            price = sell.price
            description = sell.description
            status = 'posting'
            sale_order = SaleOrder.objects.get(orderid=order_id)
            poster_id = sale_order.userid.userid
            poster_name = Users.objects.get(userid=poster_id).username
            poster = User(poster_id, poster_name)
            book = Book.objects.get(isbn=isbn)
            title = book.title
            author = book.author
            requires = Require.objects.filter(isbn=isbn)
            for require in requires:
                course_id = require.courseid.courseid
                course = Course.objects.get(courseid=course_id)
                academic_year = course.academicyear
            book_categories = BookCategory.objects.filter(isbn=isbn)
            for book_category in book_categories:
                category = book_category.category
            courseName = course.coursename
            teacherName = course.instructorname
            book_detail = {
                'isbn': isbn,
                'price': price,
                'description': description,
                'receiver': poster,
                'status': status,
                'title': title,
                'author': author,
                'category': category,
                'courseID': course_id,
                'academic_year': academic_year,
                'courseName': courseName,
                'teacherName': teacherName,
            }
            books_details.append(book_detail)

        serializer = BookDetailSerializer(data=books_details, many=True)
        serializer.is_valid()

        # Serialize the data
        serialized_data = serializer.data

        return Response({'books': serialized_data, 'user_id': user_id, 'order_id': order_id})

class ReceiveWantAPIView(APIView):
    def get(self, request, user_id, order_id, *args, **kwargs):
        books_details = []
        sells = LookFor.objects.filter(orderid=order_id)
        for sell in sells:
            isbn = sell.isbn.isbn
            status = 'posting'
            sale_order = WantOrder.objects.get(orderid=order_id)
            poster_id = sale_order.userid.userid
            poster_name = Users.objects.get(userid=poster_id).username
            poster = User(poster_id, poster_name)
            book = Book.objects.get(isbn=isbn)
            title = book.title
            author = book.author
            requires = Require.objects.filter(isbn=isbn)
            for require in requires:
                course_id = require.courseid.courseid
                course = Course.objects.get(courseid=course_id)
                academic_year = course.academicyear
            book_categories = BookCategory.objects.filter(isbn=isbn)
            for book_category in book_categories:
                category = book_category.category
            courseName = course.coursename
            teacherName = course.instructorname
            book_detail = {
                'isbn': isbn,
                'price': None,
                'description': None,
                'receiver': poster,
                'status': status,
                'title': title,
                'author': author,
                'category': category,
                'courseID': course_id,
                'academic_year': academic_year,
                'courseName': courseName,
                'teacherName': teacherName,
            }
            books_details.append(book_detail)

        serializer = BookDetailSerializer(data=books_details, many=True)
        serializer.is_valid()

        # Serialize the data
        serialized_data = serializer.data

        return Response({'books': serialized_data, 'user_id': user_id, 'order_id': order_id})


class RenewStatusAPIView(APIView):
    def post(self, request,  *args, **kwargs):
        with transaction.atomic():
            order_id = request.data.get('order_id')
            isbn = request.data.get('isbn')
            status = request.data.get('status')
            type = request.data.get('type')
            current_datetime = timezone.now()
            current_date = current_datetime.date()
            if type == 'sell':
                sell_instance = Sell.objects.select_for_update().filter(orderid__orderid=order_id, isbn__isbn=isbn).update(status=status, finishdate=current_date)
            else:
                look_for_instance = LookFor.objects.select_for_update().filter(orderid__orderid=order_id, isbn_id=isbn).update(status=status, finishdate=current_date)
            return Response()

