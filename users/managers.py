from django.contrib.auth.base_user import BaseUserManager
from django.db.models.query_utils import Q


class CustomUserManager(BaseUserManager):

    # Creat User
    def create_user(self, email, password, **kwargs):
        if email is None:
            raise TypeError('Users must have an email address.')
        user = self.model(email=self.normalize_email(email), phone=kwargs.get('phone'))
        user.set_password(password)
        user.save()
        return user

    # Create SuperUser
    def create_superuser(self, email, password, **kwargs):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(
            email=email, phone=kwargs.get('phone'), password=password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
