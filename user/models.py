
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    USER_TYPES = [('employee', 'Employee'), ('guest', 'Guest')]
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='guest')

    def __str__(self):
        return self.username
