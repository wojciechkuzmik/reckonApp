from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
	password = serializers.CharField(max_length=60, min_length=5, write_only=True)
	email = serializers.EmailField(max_length=150, min_length=4)

	class Meta:
		model = User
		fields = ['email', 'username', 'password','first_name','last_name'] 

	def validate(self, attrs):
		if len(attrs['first_name'])==0:
			raise serializers.ValidationError(
				{'first_name',('Imię nie może być puste')})
		if len(attrs['last_name'])==0:
			raise serializers.ValidationError(
				{'last_name',('Nazwisko nie może być puste')})
		if len(attrs['username'])==0:
			raise serializers.ValidationError(
				{'username',('Nazwa użytkownika nie może być pusta')})
		email = attrs.get('email', '')
		if User.objects.filter(email=email).exists():
			raise serializers.ValidationError(
				{'email',('Email is already in use')})
		return super().validate(attrs)

	def create(self, validated_data):
		return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
	password = serializers.CharField(max_length=60, min_length=5, write_only=True)
	email = serializers.EmailField(max_length=150, min_length=4)

	class Meta:
		model = User
		fields = ['email', 'username', 'password']

	def validate(self, attrs):
		email = attrs.get('email', '')
		if User.objects.filter(email=email).exists():
			raise serializers.ValidationError(
				{'email',('Email is already in use')})
		return super().validate(attrs)

	def create(self, validated_data):
		return User.objects.create_user(**validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
	password = serializers.CharField(max_length=60, min_length=5, write_only=True)
	email = serializers.EmailField(max_length=150, min_length=4)

	class Meta:
		model = User
		fields = ['email', 'username', 'password','first_name','last_name'] 

	def validate(self, attrs):
		if len(attrs['first_name'])==0:
			raise serializers.ValidationError(
				{'first_name',('Musisz podać imię')})
		if len(attrs['last_name'])==0:
			raise serializers.ValidationError(
				{'last_name',('Musisz podać nazwisko')})
		if len(attrs['username'])==0:
			raise serializers.ValidationError(
				{'username',('Musisz podać nazwę użytkownika')})
		return super().validate(attrs)
	
	def update(self, instance, validated_data):
		instance.email = validated_data.get('email', instance.email)
		instance.username = validated_data.get('username', instance.username)
		instance.first_name = validated_data.get('first_name', instance.first_name)
		instance.last_name = validated_data.get('last_name', instance.last_name)
		instance.save()
		return instance
