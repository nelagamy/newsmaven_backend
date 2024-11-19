# users/models.py
#from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)  # Auto increment primary key
    user_name = models.CharField(max_length=100)  # User's name
    email = models.EmailField(max_length=255, unique=True)  # Email, must be unique
    user_password = models.CharField(max_length=255)  # Password field

    class Meta:
        managed = False  # No migrations for this model as the table already exists in the DB
        db_table = 'User'  # Ensure this matches the name of your actual table

    def __str__(self):
        return self.user_name

