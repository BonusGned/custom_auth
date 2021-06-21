from datetime import timedelta, datetime

import jwt
from django.db import models
from django.contrib.auth.models import AbstractUser

from users.managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField('Email address', unique=True)
    phone = models.SmallIntegerField(null=True, blank=True, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    objects = CustomUserManager()

    def __str__(self):
        return self.email