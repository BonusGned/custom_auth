# import jwt
#
# from django.conf import settings

# from rest_framework import authentication, exceptions
#
from django.contrib.auth.backends import ModelBackend, BaseBackend
from django.db.models.query_utils import Q

from .models import CustomUser


class CustomModelBackend(BaseBackend):

    # Custom authenticate with phone or email
    def authenticate(self, request, **kwargs):
        try:
            if kwargs.get('phone'):
                user = CustomUser.objects.get(phone__iexact=kwargs.get('phone'))
            else:
                user = CustomUser.objects.get(
                    Q(email__iexact=kwargs.get('email')) | Q(email__iexact=kwargs.get('username')))
        except CustomUser.DoesNotExist:
            return None
        if user.check_password(kwargs.get('password')):
            return user
        return super().authenticate(request, **kwargs)

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
