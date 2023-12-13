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
from self_info.models import Book_object
from self_info.models import Book_detail
from self_info.models import Order
from rest_framework import serializers
from .models import Book_simple
from self_info.api_views import BookDetailSerializer
from .models import User


class BookSimpleSerializer(serializers.Serializer):
    isbn = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    title = serializers.CharField()
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


class UserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    user_name = serializers.CharField()
    email = serializers.EmailField()

    def create(self, validated_data):
        # Create and return a new User instance using the validated data
        return User(**validated_data)
class SaleOrderAPIView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        sale_orders_list = []
        all_sale_order = SaleOrder.objects.all()
        for i in range(1, 101):
            books = []
            sells = Sell.objects.filter(orderid=i)
            for sell in sells:
                isbn = sell.isbn.isbn
                price = sell.price
                book = Book.objects.get(isbn=isbn)
                title = book.title
                new_book = Book_simple(isbn, price, title)
                books.append(new_book)
            if books != []:
                fakeorder = Order(i, user_id, books)
                sale_orders_list.append(fakeorder)

        sale_orders_serializer = OrderSerializer(sale_orders_list, many=True)
        return Response({
            'orders': sale_orders_serializer.data,
        })

class WantOrderAPIView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        sale_orders_list = []
        for i in range(1, 101):
            books = []
            sells = LookFor.objects.filter(orderid=i)
            for sell in sells:
                isbn = sell.isbn.isbn
                book = Book.objects.get(isbn=isbn)
                title = book.title
                new_book = Book_simple(isbn, None, title)
                books.append(new_book)
            if books != []:
                fakeorder = Order(i, user_id, books)
                sale_orders_list.append(fakeorder)

        sale_orders_serializer = OrderSerializer(sale_orders_list, many=True)
        return Response({
            'orders': sale_orders_serializer.data,
        })

class SaleOrderDetailAPIView(APIView):
    def get(self, request, user_id, order_id, *args, **kwargs):
        books_details = []
        sells = Sell.objects.filter(orderid=order_id)
        for sell in sells:
            isbn = sell.isbn.isbn
            price = sell.price
            description = sell.description
            status = sell.status
            try:
                receivesale = ReceiveSale.objects.get(orderid=order_id)
                receiverid = receivesale.userid.userid
                receivername = Users.objects.get(userid=receiverid).username
                receiver = User(receiverid, receivername)
            except ReceiveSale.DoesNotExist:
                receiver = User(0, "不存在")
            book = Book.objects.get(isbn=isbn)
            title = book.title
            author = book.author
            require = Require.objects.get(isbn=isbn)
            course_id = require.courseid.courseid
            course = Course.objects.get(courseid=course_id)
            academic_year = course.academicyear
            book_category = BookCategory.objects.get(isbn=isbn)
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

        return Response({'books': serialized_data, 'user_id': user_id, 'order_id': order_id})


class WantOrderDetailAPIView(APIView):
    def get(self, request, user_id, order_id, *args, **kwargs):
        books_details = []
        sells = LookFor.objects.filter(orderid=order_id)
        for sell in sells:
            isbn = sell.isbn.isbn
            status = sell.status
            try:
                receivesale = ReceiveWant.objects.get(orderid=order_id)
                receiverid = receivesale.userid.userid
                receivername = Users.objects.get(userid=receiverid).username
                receiver = User(receiverid, receivername)
            except ReceiveWant.DoesNotExist:
                receiver = User(0, "不存在")
            book = Book.objects.get(isbn=isbn)
            title = book.title
            author = book.author
            require = Require.objects.get(isbn=isbn)
            course_id = require.courseid.courseid
            course = Course.objects.get(courseid=course_id)
            academic_year = course.academicyear
            book_category = BookCategory.objects.get(isbn=isbn)
            category = book_category.category
            courseName = course.coursename
            teacherName = course.instructorname
            book_detail = {
                'isbn': isbn,
                'price': None,
                'description': None,
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

        return Response({'books': serialized_data, 'user_id': user_id, 'order_id': order_id})

class ReceiveAPIView(APIView):
    def get(self, request, user_id, poster_id, order_id, type,  *args, **kwargs):
        poster_info = Users.objects.get(userid=poster_id)
        poster = User(poster_id, poster_info.username, poster_info.email)
        serializer = UserSerializer(poster)

        # Return the serialized data in the response
        return Response({'poster': serializer.data})