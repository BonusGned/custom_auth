from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):

    def get_serializer_class(self):
        if 'phone' in self.request.data:
            return CustomTokenObtainPairSerializer
        return TokenObtainPairSerializer
