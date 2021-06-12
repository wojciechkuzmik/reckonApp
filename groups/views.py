from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView
from django.conf import settings
from .serializers import GroupSerializer, GroupMemberSerializer, GroupsWithMembersSerializer
from rest_framework.response import Response
from rest_framework import status
import jwt
from .models import Group, Groups, Groupmembers
# Create your views here.


# create and update group
class GroupView(GenericAPIView):
    serializer_class = GroupSerializer

    def get(self, request, pk):
        token = request.headers.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        group = Groups.objects.get(groupid=pk)

        return Response(GroupsWithMembersSerializer(group).data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        token = request.headers.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        serializer = GroupSerializer(data=request.data)

        if serializer.is_valid():
            try:
                instance = Group.objects.get(groupid=pk)
            except Exception as e:
                return Response(str(e), status=status.HTTP_404_NOT_FOUND)
            serializer.update(instance, serializer.data)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        token = request.headers.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        serializer = GroupSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupMembersView(GenericAPIView):
    serializer_class = GroupMemberSerializer
    queryset = Groupmembers.objects.all()

    def get(self, request, pk):
        token = request.headers.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        group = Groups.objects.get(groupid=pk)
        return Response(GroupMemberSerializer(Groupmembers.objects.filter(groupid=group), many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        token = request.headers.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        serializer = GroupMemberSerializer(data=request.data)

        if serializer.is_valid():
            try:
                serializer.save()
            except:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        token = request.headers.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        try:
            instance = Groupmembers.objects.get(groupmemberid=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# get info about group with given groupid
class GroupInfoView(GenericAPIView):
    serializer_class = GroupsWithMembersSerializer
    queryset = Groups.objects.all()#Piotrek: dodałem to bo nie działało bez
    def get(self, request, user_id):
        token = request.headers.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        groups = Groups.objects.filter(groupid__in=Groupmembers.objects.filter(userid=user_id).values_list('groupid'))

        return Response(GroupsWithMembersSerializer(groups, many=True).data, status=status.HTTP_200_OK)




