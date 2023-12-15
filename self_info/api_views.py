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
    books = BookObjectSerializer(many=True)

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
            for sell in sells:
                if sell.status == 'Finished':
                    isbn = sell.isbn.isbn
                    price = sell.price
                    description = sell.description
                    status = 'finished'
                    try:
                        receive_sale = ReceiveSale.objects.get(orderid=order.orderid)
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

            if books != []:
                fakeorder = Order(order.orderid, user_id, books)
                sale_orders_list.append(fakeorder)

        want_orders = []
        wo = WantOrder.objects.filter(userid=user_id)
        for order in wo:
            look_for = LookFor.objects.filter(orderid=order.orderid)
            books = []
            for lf in look_for:
                if lf.status == 'Finished':
                    isbn = lf.isbn.isbn
                    status = 'finished'
                    try:
                        receive_want = ReceiveWant.objects.get(orderid=order.orderid)
                        receiverid = receive_want.userid.userid
                        receivername = Users.objects.get(userid=receiverid).username
                        receiver = User(receiverid, receivername)
                    except ReceiveWant.DoesNotExist:
                        receiver = User(0, "不存在")

                    book = Book.objects.get(isbn=isbn)
                    title = book.title
                    author = book.author
                    new_book = Book_object(isbn, None, None, receiver, status, title, author)
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
            for sell in sells:
                if sell.status == 'Posting':
                    isbn = sell.isbn.isbn
                    price = sell.price
                    description = sell.description
                    status = 'posting'
                    try:
                        receive_sale = ReceiveSale.objects.get(orderid=order.orderid)
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

            if books != []:
                fakeorder = Order(order.orderid, user_id, books)
                sale_orders_list.append(fakeorder)

        want_orders = []
        wo = WantOrder.objects.filter(userid=user_id)
        for order in wo:
            look_for = LookFor.objects.filter(orderid=order.orderid)
            books = []
            for lf in look_for:
                if lf.status == 'Posting':
                    isbn = lf.isbn.isbn
                    status = 'posting'
                    try:
                        receive_want = ReceiveWant.objects.get(orderid=order.orderid)
                        receiverid = receive_want.userid.userid
                        receivername = Users.objects.get(userid=receiverid).username
                        receiver = User(receiverid, receivername)
                    except ReceiveWant.DoesNotExist:
                        receiver = User(0, "不存在")

                    book = Book.objects.get(isbn=isbn)
                    title = book.title
                    author = book.author
                    new_book = Book_object(isbn, None, None, receiver, status, title, author)
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
        books_details = []
        sells = Sell.objects.filter(orderid=order_id)
        for sell in sells:
            if sell.status == 'Finished':
                isbn = sell.isbn.isbn
                price = sell.price
                description = sell.description
                status = 'finished'
                try:
                    receive_sale = ReceiveSale.objects.get(orderid=order_id)
                    receiverid = receive_sale.userid.userid
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

        return Response({'books': serialized_data, 'user_id': user_id, 'order_id': order_id})

class FinishWantAPIView(APIView):
    def get(self, request, user_id, order_id, *args, **kwargs):
        books_details = []
        sells = LookFor.objects.filter(orderid=order_id)
        for sell in sells:
            if sell.status == 'Finished':
                isbn = sell.isbn.isbn
                status = 'finished'
                try:
                    receive_want = ReceiveWant.objects.get(orderid=order_id)
                    receiverid = receive_want.userid.userid
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


class PostingSellAPIView(APIView):
    def get(self, request, user_id, order_id, *args, **kwargs):
        books_details = []
        sells = Sell.objects.filter(orderid=order_id)
        for sell in sells:
            if sell.status == 'Posting':
                isbn = sell.isbn.isbn
                price = sell.price
                description = sell.description
                status = 'posting'
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

class PostingWantAPIView(APIView):
    def get(self, request, user_id, order_id, *args, **kwargs):
        books_details = []
        sells = LookFor.objects.filter(orderid=order_id)
        for sell in sells:
            if sell.status == 'Posting':
                isbn = sell.isbn.isbn
                status = 'posting'
                receiver = User(0, '不存在')
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