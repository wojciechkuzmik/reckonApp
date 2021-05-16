from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import ReckoningSerializer, ReckoningPositionSerializer, CategorySerializer
from groups.serializers import GroupSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Reckonings, Users, Groups, Categories,Reckoningpositions
# Create your views here.

class CreateCategoryView(GenericAPIView):
    serializer_class = CategorySerializer

    def post(self, request):
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        serializer = CategorySerializer(data=request.data)
        response=Response(status=status.HTTP_200_OK)
        return response

class CreateReckoningView(GenericAPIView):
    serializer_class = ReckoningSerializer

    def post(self, request):
        serializer = ReckoningSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        serializer = GroupSerializer
        response=Response(status=status.HTTP_200_OK)
        response.data={
            'groups':GroupSerializer(Groups.objects.all(),many=True).data
        }
        return Response(response.data, status=status.HTTP_200_OK)#zwracam info o wszystkichgrupach które użytkownik może wybrać

class ReckoningView(GenericAPIView):

    def get(self, request, reckoning_id):

        reckoning = Reckonings.objects.get(reckoningid=reckoning_id)

        return Response(ReckoningSerializer(reckoning).data, status=status.HTTP_200_OK)

class CreateReckoningPositionView(GenericAPIView):
    serializer_class = ReckoningPositionSerializer

    def post(self, request):
        serializer = ReckoningPositionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        response=Response(status=status.HTTP_200_OK)
        response.data={
            'groups':GroupSerializer(Groups.objects.all(),many=True).data,
            'categories':CategorySerializer(Categories.objects.all(),many=True).data

        }
        return Response(response.data, status=status.HTTP_200_OK)#zwracam info o wszystkich grupach i kategoriach które użytkownik może wybrać, userzy defaultowo wszyscy z grupy są dodawani do rachunku

class ReckoningPositionsView(GenericAPIView):
    queryset=Reckoningpositions
    def get(self, request, reckoning_id):

        reckoning = Reckoningpositions.objects.filter(reckoningid=reckoning_id)

        return Response(ReckoningPositionSerializer(reckoning,many=True).data, status=status.HTTP_200_OK)
"""

Nie wiem czy to się przyda jakoś, możnaby zrobić np coś w stylu wyświetlania jednej osoby przypisanej do konretnego rachunku(reckoningposition)
class ReckoningPositionMembersView(GenericAPIView):
    queryset=Reckoningpositions
    def get(self, request, reckoningPosition_id):

        reckoning = Reckoningpositions.objects.filter(reckoningid=reckoningPosition_id)
        

        return Response(ReckoningPositionSerializer(reckoning).data, status=status.HTTP_200_OK)

"""