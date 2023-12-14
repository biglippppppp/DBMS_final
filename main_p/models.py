# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Book(models.Model):
    isbn = models.CharField(primary_key=True, max_length=13)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'book'


class BookCategory(models.Model):
    isbn = models.OneToOneField(Book, models.DO_NOTHING, db_column='isbn', primary_key=True)  # The composite primary key (isbn, category) found, that is not supported. The first column is selected.
    category = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'book_category'
        unique_together = (('isbn', 'category'),)


class Course(models.Model):
    courseid = models.CharField(primary_key=True, max_length=20)
    academicyear = models.CharField( max_length=10)  # The composite primary key (academicyear, courseid) found, that is not supported. The first column is selected.
    coursename = models.CharField(max_length=200)
    instructorname = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'course'
        unique_together = (('academicyear', 'courseid'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Evaluate(models.Model):
    evaluatoruserid = models.OneToOneField('Users', models.DO_NOTHING, db_column='evaluatoruserid', primary_key=True)  # The composite primary key (evaluatoruserid, evaluateduserid, rankdate) found, that is not supported. The first column is selected.
    evaluateduserid = models.ForeignKey('Users', models.DO_NOTHING, db_column='evaluateduserid', related_name='evaluate_evaluateduserid_set')
    ranking = models.IntegerField()
    rankdate = models.DateField()
    comment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'evaluate'
        unique_together = (('evaluatoruserid', 'evaluateduserid', 'rankdate'),)

    @classmethod
    def avg_score(cls, user_id):
        return cls.objects.filter(evaluateduserid=user_id).aggregate(models.Avg('ranking'))['ranking__avg'] or 0

class LookFor(models.Model):
    orderid = models.OneToOneField('WantOrder', models.DO_NOTHING, db_column='orderid', primary_key=True)  # The composite primary key (orderid, isbn) found, that is not supported. The first column is selected.
    isbn = models.ForeignKey(Book, models.DO_NOTHING, db_column='isbn')
    status = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    finishdate = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'look_for'
        unique_together = (('orderid', 'isbn'),)


class ReceiveSale(models.Model):
    userid = models.OneToOneField('Users', models.DO_NOTHING, db_column='userid', primary_key=True)  # The composite primary key (userid, orderid) found, that is not supported. The first column is selected.
    orderid = models.ForeignKey('SaleOrder', models.DO_NOTHING, db_column='orderid')
    receivedate = models.DateField()

    class Meta:
        managed = False
        db_table = 'receive_sale'
        unique_together = (('userid', 'orderid'),)


class ReceiveWant(models.Model):
    userid = models.OneToOneField('Users', models.DO_NOTHING, db_column='userid', primary_key=True)  # The composite primary key (userid, orderid) found, that is not supported. The first column is selected.
    orderid = models.ForeignKey('WantOrder', models.DO_NOTHING, db_column='orderid')
    receivedate = models.DateField()

    class Meta:
        managed = False
        db_table = 'receive_want'
        unique_together = (('userid', 'orderid'),)


class Require(models.Model):
    isbn = models.OneToOneField(Book, models.DO_NOTHING, db_column='isbn', primary_key=True)  # The composite primary key (isbn, courseid, academicyear) found, that is not supported. The first column is selected.
    courseid = models.ForeignKey(Course, models.DO_NOTHING, db_column='courseid', to_field='courseid')
    academicyear = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'require'
        unique_together = (('isbn', 'courseid', 'academicyear'),)


class SaleOrder(models.Model):
    orderid = models.BigIntegerField(primary_key=True)
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='userid')
    postdate = models.DateField()

    class Meta:
        managed = False
        db_table = 'sale_order'


class Sell(models.Model):
    orderid = models.OneToOneField(SaleOrder, models.DO_NOTHING, db_column='orderid', primary_key=True)  # The composite primary key (orderid, isbn) found, that is not supported. The first column is selected.
    isbn = models.ForeignKey(Book, models.DO_NOTHING, db_column='isbn')
    price = models.IntegerField()
    status = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    finishdate = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sell'
        unique_together = (('orderid', 'isbn'),)


class UserRole(models.Model):
    userid = models.OneToOneField('Users', models.DO_NOTHING, db_column='userid', primary_key=True)  # The composite primary key (userid, role) found, that is not supported. The first column is selected.
    role = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'user_role'
        unique_together = (('userid', 'role'),)


class Users(models.Model):
    userid = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=15)
    email = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'users'
        unique_together = (('username', 'email'),)


class WantOrder(models.Model):
    orderid = models.BigIntegerField(primary_key=True)
    userid = models.ForeignKey(Users, models.DO_NOTHING, db_column='userid')
    postdate = models.DateField()

    class Meta:
        managed = False
        db_table = 'want_order'