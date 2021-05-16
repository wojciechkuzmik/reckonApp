from rest_framework import serializers
from .models import Users


class UserSerializer(serializers.ModelSerializer):
	password = serializers.CharField(max_length=60, min_length=5, write_only=True)
	email = serializers.EmailField(max_length=150, min_length=4)

	class Meta:
		model = Users
		fields = ['email','userid','password','firstname','lastname'] 

	def validate(self, attrs):
		if len(attrs['firstname'])==0:
			raise serializers.ValidationError(
				{'firstname',('Imię nie może być puste')})
		if len(attrs['lastname'])==0:
			raise serializers.ValidationError(
				{'lastname',('Nazwisko nie może być puste')})
		email = attrs.get('email', '')
		if Users.objects.filter(email=email).exists():
			raise serializers.ValidationError(
				{'email',('Email is already in use')})
		return super().validate(attrs)

	def create(self, validated_data):
		return Users.objects.create(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
	password = serializers.CharField(max_length=60, min_length=5, write_only=True)
	email = serializers.EmailField(max_length=150, min_length=4)

	class Meta:
		model = Users
		fields = ['email', 'userid', 'password']

	def validate(self, attrs):
		email = attrs.get('email', '')
		if Users.objects.filter(email=email).exists():
			raise serializers.ValidationError(
				{'email',('Email is already in use')})
		return super().validate(attrs)

	def create(self, validated_data):
		return Users.objects.create(**validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
	password = serializers.CharField(max_length=60, min_length=5, write_only=True)
	email = serializers.EmailField(max_length=150, min_length=4)

	class Meta:
		model = Users
		fields = ['email', 'userid', 'password','firstname','lastname'] 

	def validate(self, attrs):
		if len(attrs['firstname'])==0:
			raise serializers.ValidationError(
				{'firstname',('Musisz podać imię')})
		if len(attrs['lastname'])==0:
			raise serializers.ValidationError(
				{'lastname',('Musisz podać nazwisko')})
		if len(attrs['email'])==0:
			raise serializers.ValidationError(
				{'email',('Musisz podać email')})
		return super().validate(attrs)
	
	def update(self, instance, validated_data):
		instance.email = validated_data.get('email', instance.email)
		instance.userid = validated_data.get('userid', instance.userid)
		instance.firstname = validated_data.get('firstname', instance.firstname)
		instance.lastname = validated_data.get('lastname', instance.lastname)
		instance.save()
		return instance


class UserSearchSerializer(serializers.ModelSerializer):
	email = serializers.EmailField(max_length=150, min_length=4)
	userid = serializers.CharField(max_length=50, min_length=2)
	firstname = serializers.CharField(max_length=50, min_length=2)
	lastname = serializers.CharField(max_length=50, min_length=2)

	class Meta:
		model = Users
		fields = ['email', 'userid', 'firstname', 'lastname']