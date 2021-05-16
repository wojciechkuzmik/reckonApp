import jwt 
from rest_framework import authentication,exceptions
from django.conf import settings
from .models import Users
from django.contrib.auth.backends import ModelBackend


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self,request):
        auth_data=authentication.get_authorization_header(request)

        if not auth_data:
            return None
        
        prefix,token=auth_data.decode('utf-8').split(' ')

        try:
            payload=jwt.decode(token,settings.JWT_SECRET_KEY)#this should be env variable

            user=Users.objects.get(username=payload['username'])

            return (user,token)

        except jwt.DecodeError as identifier:
            raise exceptions.AuthenticationFailed('Your token is invalid, login')

        except jwt.ExpiredSignatureError as identifier:
            raise exceptions.AuthenticationFailed('Your token is expired, login')

        return super().authenticate(request)


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        UserModel = Users
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.password==password:
                return user
        return None
