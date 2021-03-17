from django.db import models
from datetime import datetime
# Create your models here.


class User_role(models.Model):
    role = models.CharField(max_length=30)

    class Meta:
        db_table = "User_role"


class Users(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    photo_url = models.CharField(max_length=30)
    role = models.ForeignKey(User_role, on_delete=models.CASCADE)

    class Meta:
        db_table = "users"
        indexes = [
            models.Index(fields=['email', ])
        ]