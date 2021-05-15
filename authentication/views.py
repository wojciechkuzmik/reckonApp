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
		username=data.get('username','')
		password=data.get('password','')
		user=auth.authenticate(username=username,password=password)

		if user:
			auth_token=jwt.encode({'username':user.username},settings.JWT_SECRET_KEY,algorithm='HS256')

			serializer=UserSerializer(user)

			data={
				'user':serializer.data,'token':auth_token
			}
			response=Response()
			response.set_cookie(key='jwt',value=auth_token,httponly=True)
			response.data={
				'jwt':auth_token
			}
			return response
			#sending a response
		return Response({'detail':'Invalid credentials'},status=status.HTTP_401_UNAUTHORIZED)

	def get(self, request):
		return Response(status=status.HTTP_200_OK)
	

class UserView(APIView):
	def get(self, request):
		token=request.COOKIES.get('jwt')
		if not token:
			raise AuthenticationFailed('Unauthenticated')
		
		try:
			payload=jwt.decode(token,settings.JWT_SECRET_KEY,algorithms='HS256')
		except jwt.ExpiredSignatureError:
			raise AuthenticationFailed('Unauthenticated')
		
		user=User.objects.filter(username=payload['username']).first()
		serializer=UserSerializer(user)
		return Response(serializer.data,status=status.HTTP_200_OK)

	def put(self,request): #put dziala ale przyjmuje obiekt typu json, nie wiem jak zrobic jakis form do tego
		token=request.COOKIES.get('jwt')
		if not token:
			raise AuthenticationFailed('Unauthenticated')
		
		try:
			payload=jwt.decode(token,settings.JWT_SECRET_KEY,algorithms='HS256')
		except jwt.ExpiredSignatureError:
			raise AuthenticationFailed('Unauthenticated')
		
		user=User.objects.filter(username=payload['username']).first()
		serializer=UserUpdateSerializer(user,request.data,partial=True)
		data={}
		if serializer.is_valid():
			serializer.save()
			data['success']='successfully updated'
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
	def get(self,request):
		response=Response()
		response.delete_cookie('jwt')
		response.data={
			'message':'success'
		}
		return response


class SearchView(APIView):

	def get(self, request):
		token=request.COOKIES.get('jwt')
		if not token:
			raise AuthenticationFailed('Unauthenticated')
		
		try:
			payload=jwt.decode(token,settings.JWT_SECRET_KEY,algorithms='HS256')
		except jwt.ExpiredSignatureError:
			raise AuthenticationFailed('Unauthenticated')
		
		logged_user = User.objects.filter(username=payload['username']).first()
		username = request.data.get('username', None)
		email = request.data.get('email', None)
		first_name = request.data.get('first_name', None)
		last_name = request.data.get('last_name', None)
		users = User.objects.filter(Q(username=username) | Q(email=email) | Q(first_name=first_name) | Q(last_name=last_name)).exclude(username=logged_user.username)
		serializer = UserSearchSerializer(users, many=True)
		return Response(serializer.data,status=status.HTTP_200_OK)