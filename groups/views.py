from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import GroupSerializer, GroupMemberSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Groups, Groupmembers
# Create your views here.


class CreateGroupView(GenericAPIView):
    serializer_class = GroupMemberSerializer

    def post(self, request):
        serializer = GroupMemberSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serializer = GroupMemberSerializer(data=request.data)

        if serializer.is_valid():
            try:
                instance = Groups.objects.get(groupid=serializer.data['groupid'])
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer.update(instance, serializer.data)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupInfoView(GenericAPIView):
    serializer_class = GroupSerializer
    queryset = Groups.objects.all()#Piotrek: dodałem to bo nie działało bez
    def get(self, request, user_id):

        groups = Groups.objects.filter(groupid__in=Groupmembers.objects.filter(userid=user_id).values_list('groupid'))

        return Response(GroupSerializer(groups, many=True).data, status=status.HTTP_200_OK)


class GroupView(GenericAPIView):

    def get(self, request, group_id):

        group = Groups.objects.get(groupid=group_id)

        return Response(GroupSerializer(group).data, status=status.HTTP_200_OK)


