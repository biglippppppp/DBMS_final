from django.db import models

# Create your models here.
class User:
    def __init__(self, user_id, user_name, role='user'):
        self.user_id = user_id
        self.user_name = user_name
        self.role = role


class Book_object:
    def __init__(self, isbn, price, description, receiver, status, title, author):
        self.isbn = isbn
        self.price = price
        self.description = description
        self.status = status
        self.receiver = receiver
        self.title = title
        self.author = author


class Order:
    def __init__(self, order_id, user_id, books):
        self.order_id = order_id
        self.user_id = user_id
        self.books = books

    class Meta:
        managed = True


class Book_detail:
    def __init__(self, isbn, price, description, receiver, status,
                 title, author, category, courseID, academic_year, course_name, teacher_name):
        self.isbn = isbn
        self.price = price
        self.description = description
        self.status = status
        self.receiver = receiver
        self.title = title
        self.author = author
        self.category = category
        self.courseID = courseID
        self.academic_year = academic_year
        self.courseName = course_name
        self.teacherName = teacher_name