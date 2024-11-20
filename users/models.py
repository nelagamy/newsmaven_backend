# users/models.py
#from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


# class User(models.Model):
#     user_id = models.AutoField(primary_key=True)  # Auto increment primary key
#     user_name = models.CharField(max_length=100)  # User's name
#     email = models.EmailField(max_length=255, unique=True)  # Email, must be unique
#     user_password = models.CharField(max_length=255)  # Password field

#     class Meta:
#         managed = False  # No migrations for this model as the table already exists in the DB
#         db_table = 'User'  # Ensure this matches the name of your actual table

#     def __str__(self):
#         return self.user_name

class User(models.Model):
    user_id = models.AutoField(primary_key=True)  # Auto increment primary key
    user_name = models.CharField(max_length=100)  # User's name
    email = models.EmailField(max_length=255, unique=True)  # Email, must be unique
    user_password = models.CharField(max_length=255)  # Password field (stored as hash)

    class Meta:
        managed = False  # No migrations for this model as the table already exists in the DB
        db_table = 'User'  # Ensure this matches the name of your actual table

    def __str__(self):
        return self.user_name

    def set_password(self, raw_password):
        self.user_password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.user_password)


class HistoryTitle(models.Model):
    chat_id = models.AutoField(primary_key=True)
    chat_name = models.CharField(max_length=255)
    time_stamp = models.DateTimeField()
    user_id = models.IntegerField()

    class Meta:
        db_table = 'History_Title'  # Match your database table name
        managed = False  # Since it's an existing table

class Chat(models.Model):
    chat_message_id = models.AutoField(primary_key=True)
    chat_text = models.TextField()
    chat_id = models.IntegerField()
    sender_type = models.CharField(max_length=6, choices=[('user', 'user'), ('agent', 'agent')])
    time_stamp = models.DateTimeField()

    class Meta:
        db_table = 'Chat'  # Match your database table name
        managed = False  # Since it's an existing table


