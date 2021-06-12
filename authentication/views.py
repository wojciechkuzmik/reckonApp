from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import UserSerializer, UserUpdateSerializer, UserSearchSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.db.models import Q
from .models import Users
from .backends import authentication

# Create your views here.
class RegisterView(GenericAPIView):
	serializer_class = UserSerializer

	def post(self, request):
		serializer = UserSerializer(data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def get(self, request):
		return Response(status=status.HTTP_200_OK)


class LoginView(GenericAPIView):
	serializer_class = UserSerializer
	def post(self,request):
		data=request.data
		email=data.get('email','')
		password=data.get('password','')
		user=auth.authenticate(username=email,password=password)
		if user:
			auth_token=jwt.encode({'email':user.email},settings.JWT_SECRET_KEY,algorithm='HS256')

			serializer=UserSerializer(user)

			data={
				'user':serializer.data,'token':auth_token
			}
			response=Response()
			response.set_cookie(key='jwt',value=auth_token)
			response.data={
				'jwt':auth_token
			}
			return response
			#sending a response
		return Response({'detail':'[Invalid credentials]'},status=status.HTTP_401_UNAUTHORIZED)

	def get(self, request):
		return Response(status=status.HTTP_200_OK)
	

class UserView(APIView):
	def get(self, request):
		token = request.headers.get('jwt')
		if not token:
			raise AuthenticationFailed('Unauthenticated')

		try:
			payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms='HS256')
		except jwt.ExpiredSignatureError:
			raise AuthenticationFailed('Unauthenticated')
		
		user=Users.objects.filter(email=payload['email']).first()
		serializer=UserSerializer(user)
		return Response(serializer.data,status=status.HTTP_200_OK)

	def put(self,request):
		token=request.headers.get('jwt')
		if not token:
			raise AuthenticationFailed('Unauthenticated')
		
		try:
			payload=jwt.decode(token,settings.JWT_SECRET_KEY,algorithms='HS256')
		except jwt.ExpiredSignatureError:
			raise AuthenticationFailed('Unauthenticated')
		
		user=Users.objects.filter(email=payload['email']).first()
		serializer=UserUpdateSerializer(user,request.data,partial=True)
		data={}
		if serializer.is_valid():
			serializer.save()
			data['success']='successfully updated'
			#update user info in jwt
			auth_token=jwt.encode({'email':user.email},settings.JWT_SECRET_KEY,algorithm='HS256')

			serializer=UserSerializer(user)

			data={
				'user':serializer.data,'token':auth_token
			}
			response=Response(status=status.HTTP_200_OK)
			response.set_cookie(key='jwt',value=auth_token,httponly=True)
			response.data={
				'jwt':auth_token
			}
			#end
			return response
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
	def get(self,request):
		response=Response(status=status.HTTP_200_OK)
		response.delete_cookie('jwt')
		response.data={
			'message':'success'
		}
		return response


class SearchView(APIView):

	def get(self, request):
		token = request.headers.get('jwt')
		if not token:
			raise AuthenticationFailed('Unauthenticated')

		try:
			payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms='HS256')
		except jwt.ExpiredSignatureError:
			raise AuthenticationFailed('Unauthenticated')
		
		logged_user = Users.objects.filter(email=payload['email']).first()
		userid = request.GET.get('userid')
		email = request.GET.get('email')
		firstname = request.GET.get('firstname')
		lastname = request.GET.get('lastname')
		users = Users.objects.filter(Q(userid=userid) | Q(email=email) | Q(firstname=firstname) | Q(lastname=lastname)).exclude(userid=logged_user.userid)
		serializer = UserSearchSerializer(users, many=True)
		return Response(serializer.data,status=status.HTTP_200_OK)