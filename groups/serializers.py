from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from rest_framework import serializers
from .models import Groups, Users, Groupmembers, Roles
from datetime import datetime


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ['userid', 'firstname', 'lastname', 'email']


class UserSerializerShort(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ['email']

class GroupMemberSerializerShort(serializers.ModelSerializer):

    class Meta:
        model = Groupmembers
        fields = ['groupmemberid']


class GroupMemberSerializer(serializers.ModelSerializer):
    members = UserSerializerShort(many=True, required=False, allow_null=True)
    groupid = serializers.IntegerField(required=False)

    class Meta:
        model = Groups
        fields = ['groupid', 'name', 'startdate', 'members']

    def validate(self, attrs):
        if len(attrs['name']) == 0:
            raise serializers.ValidationError(
                {'name', ('Musisz podać nazwę')}
            )
        if 'members' in attrs:
            members = attrs['members']
            for member in members:
                try:
                    user = Users.objects.get(email=member['email'])
                except ObjectDoesNotExist or MultipleObjectsReturned:
                    raise serializers.ValidationError({'members', 'Incorrect group member: ' + member['email']})

        return super().validate(attrs)

    def create(self, validated_data):
        members = validated_data.pop('members', None)
        instance = Groups.objects.create(**validated_data)

        if members is not None:
            for member in members:
                user = Users.objects.get(email=member['email'])
                Groupmembers.objects.create(
                    groupid=instance,
                    roleid=Roles.objects.get(roleid=1),
                    userid=user,
                    adddate=datetime.now())
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.startdate = validated_data['startdate']
        instance.save()
        Groupmembers.objects.filter(groupid=instance.groupid).delete()

        members = validated_data.pop('members', None)
        if members is not None:
            for member in members:
                user = Users.objects.get(email=member['email'])
                Groupmembers.objects.create(
                    groupid=instance,
                    roleid=Roles.objects.get(roleid=1),
                    userid=user,
                    adddate=datetime.now())

        return instance


class GroupSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = Groups
        fields = ['groupid', 'name', 'startdate', 'members']




