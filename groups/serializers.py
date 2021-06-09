from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import Group, Groups, Users, Groupmembers
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


class GroupsWithMembersSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True)

    class Meta:
        model = Groups
        fields = ['groupid', 'name', 'startdate', 'members']

    """
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
                    userid=user,
                    adddate=datetime.now())
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.startdate = validated_data['startdate']
        instance.save()

        return instance

"""


class GroupMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Groupmembers
        fields = ['groupmemberid', 'groupid', 'userid', 'adddate', 'isactive']

    def validate(self, attrs):
        if 'groupmemberid' in attrs:
            if len(attrs['groupmemberid']) == 0:
                raise serializers.ValidationError(
                    {'groupmemberid', ('Group memberid id must not be blank')}
                )
            try:
                groupmember = Groupmembers.objects.get(groupmemberid=attrs['groupmemberid'])
            except ObjectDoesNotExist:
                raise serializers.ValidationError({'groupmemberid', 'Incorrect group member id: ' + attrs['groupmemberid']})

        return super().validate(attrs)

    def create(self, validated_data):
        group = validated_data.pop('groupid', None)
        user = validated_data.pop('userid', None)
        if group is None:
            raise serializers.ValidationError(
                {'groupid': 'If you want to create group member, provide group id'}
            )
        if user is None:
            raise serializers.ValidationError(
                {'userid': 'If you want to create group member, provide user id'}
            )

        instance = Groupmembers.objects.create(
            groupid=group,
            userid=user,
            adddate=datetime.now()
        )
        return instance


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['groupid', 'name', 'startdate']

    def validate(self, attrs):
        if len(attrs['name']) == 0:
            raise serializers.ValidationError(
                {'name', ('Musisz podać nazwę')}
            )
        return super().validate(attrs)

    def create(self, validated_data):
        instance = Group.objects.create(
            name=validated_data.pop('name'),
            startdate=datetime.now()
        )
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.pop('name')
        instance.save()
        return instance


