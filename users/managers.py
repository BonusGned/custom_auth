from django.contrib.auth.base_user import BaseUserManager
from django.db.models.query_utils import Q


class CustomUserManager(BaseUserManager):

    def create_user(self, email, phone, password):
        if email is None:
            raise TypeError('Users must have an email address.')

        if phone is None:
            raise TypeError('Users must have a phone.')

        user = self.model(email=self.normalize_email(email), phone=phone)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, phone, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(
            email=email, phone=phone, password=password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user