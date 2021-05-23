from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from rest_framework import serializers
from .models import Groups, Users, Groupmembers, Reckonings,Reckoningpositions
from groups.serializers import GroupMemberSerializer, GroupSerializer
from datetime import datetime


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
        autor_groupmember=validated_data.pop('author')
        id_user_received=GroupMemberSerializer(autor_groupmember).data['groupmemberid']
        grp_id=validated_data.pop('groupid')
        gr_id=GroupSerializer(grp_id).data['groupid']
        group_member=Groupmembers.objects.filter(groupid=gr_id).filter(userid=id_user_received)[0]
        full_data={
        "name":validated_data.pop('name'),
        "startdate":datetime.now(),
        "deadline":validated_data.pop('deadline'),
        "groupid":grp_id,
        "author":group_member
         }
        instance = Reckonings.objects.create(**full_data)
        return instance


class ReckoningPositionSerializer(serializers.ModelSerializer):
    #jak na razie to jest nieaktywne. Bo nie dodajemy wszystkich userów z grupy do pozycji tylko po jednym.
    class Meta:
        model = Reckoningpositions
        fields = ['reckoningpositionid', 'name', 'amount','groupmemberid','reckoningid','paymentdate']
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
        group_members=Groupmembers.objects.all().filter(groupid=group_id[0][0]).values_list('groupmemberid')
        name=validated_data.pop('name')
        amount=validated_data.pop('amount')
        paymentdate=validated_data.pop('paymentdate')
        for i in group_members:
            full_data={
                "name":name,
                "amount":amount,
                "reckoningid":Reckonings.objects.get(reckoningid=rec_id),
                "groupmemberid":Groupmembers.objects.get(groupmemberid=i[0]),
                "paymentdate":paymentdate
                }
            instance = Reckoningpositions.objects.create(**full_data)
        return instance

class ReckoningPositionForOneUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reckoningpositions
        fields = ['reckoningpositionid', 'name', 'amount','groupmemberid','reckoningid','paymentdate']
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
        group_id=Reckonings.objects.filter(reckoningid=rec_id).values_list('groupid')[0]
        name=validated_data.pop('name')
        amount=validated_data.pop('amount')
        paymentdate=validated_data.pop('paymentdate')
        member_to_add=validated_data.pop('groupmemberid')
        id_user_received=GroupMemberSerializer(member_to_add).data['groupmemberid']
        group_member=Groupmembers.objects.filter(groupid=group_id).filter(userid=id_user_received)[0]
        full_data={
            "name":name,
            "amount":amount,
            "reckoningid":Reckonings.objects.get(reckoningid=rec_id),
            "groupmemberid":group_member,
            "paymentdate":paymentdate
            }
        instance = Reckoningpositions.objects.create(**full_data)
        return instance