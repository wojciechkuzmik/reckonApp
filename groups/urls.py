from django.urls import path
from .views import CreateGroupView, GroupView, GroupInfoView

urlpatterns = [
	path('group', CreateGroupView.as_view()),	#create group
	path('group/<int:group_id>', GroupView.as_view()),	#get info about group with id
	path('groupinfo/<int:user_id>', GroupInfoView.as_view())	#get info about all groups for user with id
]