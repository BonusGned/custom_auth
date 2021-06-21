from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import CustomUser

from django.contrib.auth import authenticate


class CustomTokenObtainPairSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['phone', 'password']

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        authenticate_kwargs = {
            'phone': attrs['phone'],
            'password': attrs['password'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass
        user = authenticate(phone=authenticate_kwargs.get('phone'), password=authenticate_kwargs.get('password'))
        if user:
            refresh = self.get_token(user)
            data = {'refresh': str(refresh), 'access': str(refresh.access_token)}
            return data
        elif not user:
            return 'User does not exist'
