from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from rest_framework import serializers
from .models import Groups, Users, Groupmembers, Reckonings, Categories,Reckoningpositions
from groups.serializers import GroupMemberSerializer
from datetime import datetime

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['categoryid', 'name']
    def validate(self, attrs):
        if len(attrs['name']) == 0:
            raise serializers.ValidationError(
                {'name', ('Musisz podać nazwę')}
            )
        return super().validate(attrs)
    def create(self, validated_data):
        instance = Categories.objects.create(**validated_data)
        return instance
    

class ReckoningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reckonings
        fields = ['reckoningid', 'name', 'startdate', 'deadline','groupid', 'author']
    
    def validate(self, attrs):
        if len(attrs['name']) == 0:
            raise serializers.ValidationError(
                {'name', ('Musisz podać nazwę')}
            )
        return super().validate(attrs)

    def create(self, validated_data):
        full_data={
        "name":validated_data.pop('name'),
        "startdate":datetime.now(),
        "deadline":validated_data.pop('deadline'),
        "groupid":validated_data.pop('groupid'),
        "author":validated_data.pop('author')
         }
        instance = Reckonings.objects.create(**full_data)
        return instance


class ReckoningPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reckoningpositions
        fields = ['reckoningpositionid', 'name', 'amount', 'categoryid','groupmemberid','reckoningid','paymentdate']
    def validate(self, attrs):
        if len(attrs['name']) == 0:
            raise serializers.ValidationError(
                {'name', ('Musisz podać nazwę')}
            )
        if attrs['amount']<0 or not isinstance(attrs['amount'], float):
            raise serializers.ValidationError(
                {'amount', ('Musisz podać prawidłową kwotę')}
            )
        return super().validate(attrs)

    def create(self, validated_data):
        rec_id=validated_data.pop('reckoningid').reckoningid
        group_id=Reckonings.objects.filter(reckoningid=rec_id).values_list('groupid')
        group_members=Groupmembers.objects.all().filter(groupid=group_id[0][0]).values_list('groupmemberid')#stąd trzeba wykluczyć wybranych ludzi z grupy i elo, tylko nie wiem jak
        name=validated_data.pop('name')
        amount=validated_data.pop('amount')
        cat_id=validated_data.pop('categoryid')
        paymentdate=validated_data.pop('paymentdate')
        for i in group_members:
            full_data={
                "name":name,
                "amount":amount,
                "reckoningid":Reckonings.objects.get(reckoningid=rec_id),
                "categoryid":cat_id,
                "groupmemberid":Groupmembers.objects.get(groupmemberid=i[0]),
                "paymentdate":paymentdate
                }
            instance = Reckoningpositions.objects.create(**full_data)
        return instance

class ReckoningPositionForOneUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reckoningpositions
        fields = ['reckoningpositionid', 'name', 'amount', 'categoryid','groupmemberid','reckoningid','paymentdate']
    def validate(self, attrs):
        if len(attrs['name']) == 0:
            raise serializers.ValidationError(
                {'name', ('Musisz podać nazwę')}
            )
        if attrs['amount']<0 or not isinstance(attrs['amount'], float):
            raise serializers.ValidationError(
                {'amount', ('Musisz podać prawidłową kwotę')}
            )
        return super().validate(attrs)

    def create(self, validated_data):
        rec_id=validated_data.pop('reckoningid').reckoningid
        group_id=Reckonings.objects.filter(reckoningid=rec_id).values_list('groupid')
        name=validated_data.pop('name')
        amount=validated_data.pop('amount')
        cat_id=validated_data.pop('categoryid')
        paymentdate=validated_data.pop('paymentdate')
        member_to_add=validated_data.pop('groupmemberid')
        full_data={
            "name":name,
            "amount":amount,
            "reckoningid":Reckonings.objects.get(reckoningid=rec_id),
            "categoryid":cat_id,
            "groupmemberid":member_to_add,
            "paymentdate":paymentdate
            }
        instance = Reckoningpositions.objects.create(**full_data)
        return instance