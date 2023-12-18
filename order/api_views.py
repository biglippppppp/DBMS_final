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
from self_info.models import User
from evaluate.api_views import UsersSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.http import Http404


class BookDetailSerializer(serializers.Serializer):
    isbn = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField()
    status = serializers.CharField()
    receiver = serializers.CharField()
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
    def get(self, request, user_id, page, *args, **kwargs):

        # Get all sale orders
        all_sale_orders = SaleOrder.objects.all()

        # Paginate the sale orders
        paginator = Paginator(all_sale_orders, self.get_items_per_page())
        try:
            sale_orders = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            raise Http404("Invalid page number")

        sale_orders_list = []

        # Iterate through the sale orders
        for sale_order in sale_orders:
            books = self.get_books_for_sale_order(sale_order)
            if books:
                fake_order = self.get_fake_order_serializer(sale_order, user_id, books).data
                sale_orders_list.append(fake_order)

        # Serialize the sale orders
        sale_orders_serializer = OrderSerializer(sale_orders_list, many=True)

        return Response({'orders': sale_orders_serializer.data})

    def get_items_per_page(self):
        # Implement your logic for determining items per page
        return 20

    def get_books_for_sale_order(self, sale_order):
        books = []
        sells = Sell.objects.filter(orderid=sale_order.orderid)
        for sell in sells:
            isbn = sell.isbn.isbn
            price = sell.price
            book = Book.objects.get(isbn=isbn)
            title = book.title
            new_book = BookSimpleSerializer({'isbn': isbn, 'price': price, 'title': title}).data
            books.append(new_book)
        return books

    def get_fake_order_serializer(self, sale_order, user_id, books):
        return OrderSerializer({'order_id': sale_order.orderid, 'user_id': user_id, 'books': books})

class WantOrderAPIView(APIView):
    def get(self, request, user_id, page, *args, **kwargs):
        # Get all sale orders
        all_sale_orders = WantOrder.objects.all()

        # Paginate the sale orders
        paginator = Paginator(all_sale_orders, self.get_items_per_page())
        try:
            sale_orders = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            raise Http404("Invalid page number")

        sale_orders_list = []

        # Iterate through the sale orders
        for sale_order in sale_orders:
            books = self.get_books_for_sale_order(sale_order)
            if books:
                fake_order = self.get_fake_order_serializer(sale_order, user_id, books).data
                sale_orders_list.append(fake_order)

        # Serialize the sale orders
        sale_orders_serializer = OrderSerializer(sale_orders_list, many=True)

        return Response({'orders': sale_orders_serializer.data})

    def get_items_per_page(self):
        # Implement your logic for determining items per page
        return 20

    def get_books_for_sale_order(self, sale_order):
        books = []
        sells = LookFor.objects.filter(orderid=sale_order.orderid)
        for sell in sells:
            isbn = sell.isbn.isbn
            price = None
            book = Book.objects.get(isbn=isbn)
            title = book.title
            new_book = BookSimpleSerializer({'isbn': isbn, 'price': price, 'title': title}).data
            books.append(new_book)
        return books

    def get_fake_order_serializer(self, sale_order, user_id, books):
        return OrderSerializer({'order_id': sale_order.orderid, 'user_id': user_id, 'books': books})


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
    def post(self, request, user_id, poster_id, order_id, type,  *args, **kwargs):
        poster_info = Users.objects.get(userid=poster_id)
        serializer = UsersSerializer(poster_info)
        current_datetime = timezone.now()
        current_date = current_datetime.date()
        if type == 'sale_order':
            sell_instance = ReceiveSale.objects.filter(orderid__orderid=order_id)
            sell_instance.userid = user_id
            sell_instance.reseivedate = current_date
            sell_instance.save()
        else:
            instance = LookFor.objects.filter(orderid__orderid=order_id)
            instance.userid = user_id
            instance.reseivedate = current_date
            instance.save()


        # Return the serialized data in the response
        return Response({'poster': serializer.data})