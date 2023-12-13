from django.db import models

# Create your models here.
class Book_simple:
    def __init__(self, isbn, price, title):
        self.isbn = isbn
        self.price = price
        self.title = title


class User:
    def __init__(self, user_id, user_name, email, role='user'):
        self.user_id = user_id
        self.user_name = user_name
        self.role = role
        self.email = email