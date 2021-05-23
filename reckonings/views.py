from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import ReckoningSerializer, ReckoningPositionSerializer, CategorySerializer,GroupMemberSerializer, ReckoningPositionForOneUserSerializer
from groups.serializers import GroupSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Reckonings, Users, Groups, Categories,Reckoningpositions,Groupmembers
# Create your views here.

class CreateCategoryView(GenericAPIView):
    serializer_class = CategorySerializer

    def post(self, request):
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CategoriesView(GenericAPIView):
    serializer_class = CategorySerializer
    
    def get(self, request):
        serializer = CategorySerializer(data=request.data)
        response=Response()
        response.data={
            'categories':CategorySerializer(Categories.objects.all(),many=True).data
        }
        return Response(response.data, status=status.HTTP_200_OK)

class CategoryView(GenericAPIView):
    serializer_class = CategorySerializer
    
    def get(self, request, cat_id):
        serializer = CategorySerializer(data=request.data)
        response=Response()
        response.data={
            'categories':CategorySerializer(Categories.objects.get(categoryid=cat_id)).data
        }
        return Response(response.data, status=status.HTTP_200_OK)


class CreateReckoningView(GenericAPIView):
    serializer_class = ReckoningSerializer

    def post(self, request):
        serializer = ReckoningSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #info o tym, jakie grupy może wybrać użytkownik jest w endpointach Pawła

class ReckoningView(GenericAPIView):

    def get(self, request, reckoning_id):

        reckoning = Reckonings.objects.get(reckoningid=reckoning_id)

        return Response(ReckoningSerializer(reckoning).data, status=status.HTTP_200_OK)

class ReckoningsInGroupView(GenericAPIView):
    queryset=Reckonings
    def get(self, request, group_id):
        
        reckoning = Reckonings.objects.filter(groupid=group_id).order_by('-startdate')

        reckoning_ids={}
        for i in reckoning:
            reckoning_ids[ReckoningSerializer(i).data['reckoningid']]="NO"
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

        return Response(reckonings, status=status.HTTP_200_OK)

class CreateReckoningPositionView(GenericAPIView):
    serializer_class = ReckoningPositionSerializer

    def post(self, request):
        serializer = ReckoningPositionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateReckoningPositionForOneView(GenericAPIView):
    serializer_class = ReckoningPositionForOneUserSerializer

    def post(self, request):
        serializer = ReckoningPositionForOneUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReckoningPositionsView(GenericAPIView):
    queryset=Reckoningpositions
    def get(self, request, reckoning_id):

        reckoning = Reckoningpositions.objects.filter(reckoningid=reckoning_id)
        return Response(ReckoningPositionSerializer(reckoning,many=True).data, status=status.HTTP_200_OK)

class ReckoningPositionsForUserView(GenericAPIView):
    queryset=Groupmembers
    def get(self, request, user_id):
        group_member_ids_for_user=Groupmembers.objects.filter(userid=user_id)
        group_member_ids_for_user=group_member_ids_for_user.values('groupmemberid')
        ids=[]
        for i in group_member_ids_for_user:
            ids.append(i["groupmemberid"])
        #print(group_member_ids_for_user)
        reckoning = Reckoningpositions.objects.filter(groupmemberid__in=ids)
        return Response(ReckoningPositionSerializer(reckoning,many=True).data, status=status.HTTP_200_OK)

class ReckoningPositionsByUserView(GenericAPIView):
    queryset=Reckoningpositions
    def get(self, request, user_id):
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
        return Response(ReckoningPositionSerializer(reckoningPositionsByUser,many=True).data, status=status.HTTP_200_OK)


"""

Nie wiem czy to się przyda jakoś, możnaby zrobić np coś w stylu wyświetlania jednej osoby przypisanej do konretnego rachunku(reckoningposition)
class ReckoningPositionMembersView(GenericAPIView):
    queryset=Reckoningpositions
    def get(self, request, reckoningPosition_id):

        reckoning = Reckoningpositions.objects.filter(reckoningid=reckoningPosition_id)
        

        return Response(ReckoningPositionSerializer(reckoning).data, status=status.HTTP_200_OK)

"""