import jwt
from django.conf import settings
from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView
from .serializers import ReckoningSerializer, ReckoningPositionSerializer,GroupMemberSerializer, ReckoningPositionForOneUserSerializer
from groups.serializers import GroupSerializer,UserSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Reckonings, Users, Groups, Reckoningpositions,Groupmembers
# Create your views here.

class GroupMemberUserView(GenericAPIView):

    def get(self, request, groupmemberid):

        reckoning = Groupmembers.objects.get(groupmemberid=groupmemberid)

        return Response(GroupMemberSerializer(reckoning).data, status=status.HTTP_200_OK)

class CreateReckoningView(GenericAPIView):
    serializer_class = ReckoningSerializer

    def post(self, request):
        print(request.data)
        grp_id=request.data['groupid']
        id_user_received=request.data['author']
        group_member=GroupMemberSerializer( Groupmembers.objects.filter(groupid=grp_id).filter(userid=id_user_received),many=True).data[0]['groupmemberid']
        request.data['author']=group_member
        serializer = ReckoningSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #info o tym, jakie grupy może wybrać użytkownik jest w endpointach Pawła

class ReckoningView(GenericAPIView):

    def get(self, request, reckoning_id):
        reckoning = Reckonings.objects.get(reckoningid=reckoning_id)
        groupmemberid=ReckoningSerializer(reckoning).data['author']
        grpmember=GroupMemberSerializer(Groupmembers.objects.filter(groupmemberid=groupmemberid),many=True)
        reckoninginfo=ReckoningSerializer(reckoning).data
        reckoninginfo["autor"]=grpmember.data
        reck_inf_autor=reckoninginfo["autor"]
        userid=reck_inf_autor[0]['userid']
        userinfo=UserSerializer(Users.objects.get(userid=userid)).data
        reckoninginfo["autor_details"]=userinfo
        return Response(reckoninginfo, status=status.HTTP_200_OK)

class ReckoningsInGroupView(GenericAPIView):
    queryset=Reckonings
    def get(self, request, group_id):
        token = request.headers.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        reckoning = Reckonings.objects.filter(groupid=group_id).order_by('-startdate')

        reckoning_ids={}
        for i in reckoning:
            reckoning_ids[ReckoningSerializer(i).data['reckoningid']]="DoesNotMatter"
        for i in reckoning_ids.keys():
            payed="False"
            all_payed="True"
            for j in ReckoningPositionSerializer(Reckoningpositions.objects.filter(reckoningid=i),many=True).data:
                if j['paymentdate']==None:
                    all_payed="False"
                else:
                    payed="PARTIAL"
            if all_payed=="True":
                reckoning_ids[i]="True"
            elif all_payed=="False" and payed=="PARTIAL":
                reckoning_ids[i]="PARTIAL"
            else:
                reckoning_ids[i]="False"
        
        reckonings=ReckoningSerializer(reckoning,many=True).data
        for item in reckonings:
            item['payment_status']=reckoning_ids[item['reckoningid']]
            author_id=item['author']
            grpmember=GroupMemberSerializer(Groupmembers.objects.filter(groupmemberid=author_id),many=True)
            reck_inf_autor=grpmember.data
            userid=reck_inf_autor[0]['userid']
            userinfo=UserSerializer(Users.objects.get(userid=userid)).data
            item['author_detail']=userinfo

        return Response(reckonings, status=status.HTTP_200_OK)

class CreateReckoningPositionView(GenericAPIView):
    serializer_class = ReckoningPositionSerializer

    def post(self, request):
        token = request.headers.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        serializer = ReckoningPositionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateReckoningPositionForOneView(GenericAPIView):
    serializer_class = ReckoningPositionForOneUserSerializer

    def post(self, request):
        token = request.headers.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        rec_id=request.data['reckoningid']
        group_id=Reckonings.objects.filter(reckoningid=rec_id).values_list('groupid')[0]
        id_user_received=request.data['groupmemberid']
        print(group_id,id_user_received)
        group_member=Groupmembers.objects.filter(groupid=group_id).filter(userid=id_user_received)[0]
        request.data['groupmemberid']=GroupMemberSerializer(group_member).data['groupmemberid']

        serializer = ReckoningPositionForOneUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReckoningPositionsView(GenericAPIView):
    queryset=Reckoningpositions
    def get(self, request, reckoning_id):
        token = request.headers.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        reckoning = Reckoningpositions.objects.filter(reckoningid=reckoning_id)
        response_data=ReckoningPositionSerializer(reckoning,many=True).data
        for item in response_data:
            author_id=item['groupmemberid']
            grpmember=GroupMemberSerializer(Groupmembers.objects.filter(groupmemberid=author_id),many=True)
            reck_inf_autor=grpmember.data
            userid=reck_inf_autor[0]['userid']
            userinfo=UserSerializer(Users.objects.get(userid=userid)).data
            item['author_detail']=userinfo
        return Response(response_data, status=status.HTTP_200_OK)

class ReckoningPositionsForUserView(GenericAPIView):
    queryset=Groupmembers
    def get(self, request, user_id):
        token = request.headers.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        group_member_ids_for_user=Groupmembers.objects.filter(userid=user_id)
        group_member_ids_for_user=group_member_ids_for_user.values('groupmemberid')
        ids=[]
        for i in group_member_ids_for_user:
            ids.append(i["groupmemberid"])
        #print(group_member_ids_for_user)
        reckoning = Reckoningpositions.objects.filter(groupmemberid__in=ids)
        response_data=ReckoningPositionSerializer(reckoning,many=True).data
        for item in response_data:
            author_id=item['groupmemberid']
            grpmember=GroupMemberSerializer(Groupmembers.objects.filter(groupmemberid=author_id),many=True)
            reck_inf_autor=grpmember.data
            userid=reck_inf_autor[0]['userid']
            userinfo=UserSerializer(Users.objects.get(userid=userid)).data
            item['author_detail']=userinfo
        return Response(response_data, status=status.HTTP_200_OK)

class ReckoningPositionsByUserView(GenericAPIView):
    queryset=Reckoningpositions
    def get(self, request, user_id):
        token = request.headers.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        group_member_ids_for_user=Groupmembers.objects.filter(userid=user_id)
        group_member_ids_for_user=group_member_ids_for_user.values('groupmemberid')
        ids=[]
        for i in group_member_ids_for_user:
            ids.append(i["groupmemberid"])
        #print(group_member_ids_for_user)
        reckoning = Reckonings.objects.filter(author__in=ids)
        ids=[]
        for i in reckoning.values('reckoningid'):
            ids.append(i["reckoningid"])
        reckoningPositionsByUser=Reckoningpositions.objects.filter(reckoningid__in=ids)
        response_data=ReckoningPositionSerializer(reckoningPositionsByUser,many=True).data
        for item in response_data:
            author_id=item['groupmemberid']
            grpmember=GroupMemberSerializer(Groupmembers.objects.filter(groupmemberid=author_id),many=True)
            reck_inf_autor=grpmember.data
            userid=reck_inf_autor[0]['userid']
            userinfo=UserSerializer(Users.objects.get(userid=userid)).data
            item['author_detail']=userinfo
        return Response(response_data, status=status.HTTP_200_OK)
