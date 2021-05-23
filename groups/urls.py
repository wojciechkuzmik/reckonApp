from django.urls import path
from .views import GroupView, GroupMembersView, GroupInfoView

urlpatterns = [
	path('group', GroupView.as_view()),	# create group
	path('group/<int:pk>', GroupView.as_view()),	# get info about group with id
	path('groupmembers', GroupMembersView.as_view()), # add/delete members from view
	path('groupmembers/<int:pk>', GroupMembersView.as_view()),  # add/delete members from view
	path('groupinfo/<int:user_id>', GroupInfoView.as_view()) # get info about all groups for user with id
]