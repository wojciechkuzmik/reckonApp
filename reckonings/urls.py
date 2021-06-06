from django.urls import path
from .views import CreateReckoningView,ReckoningView,CreateReckoningPositionView, ReckoningPositionsView,ReckoningsInGroupView, ReckoningPositionsForUserView,ReckoningPositionsByUserView, CreateReckoningPositionForOneView,GroupMemberUserView
#ReckoningPositionMembersView

urlpatterns = [
	path('GroupMemberUser/<groupmemberid>',GroupMemberUserView.as_view()),
	path('reckoning', CreateReckoningView.as_view()),	#create reckoning
	path('reckoning/<int:reckoning_id>',ReckoningView.as_view()),#get info about reckoning 
	path('reckonings_in_group/<int:group_id>',ReckoningsInGroupView.as_view()),#get info about reckonings in group
	#path('reckoningPositionForAll', CreateReckoningPositionView.as_view()),	#create reckoningPosition FOR ALL USERS IN GROUP CONNECTED TO THIS RECKONING!!!
	path('reckoningPosition', CreateReckoningPositionForOneView.as_view()),#create reckoningPosition FOR ONE SPECIFIED USER
	path('reckoningPosition/<int:reckoning_id>', ReckoningPositionsView.as_view()),	#get info about reckoning positions in reckoning
	path('reckoningPositionsForUser/<int:user_id>',ReckoningPositionsForUserView.as_view()),#get info about reckoning positions that user has to pay
	path('reckoningPositionsByUser/<int:user_id>',ReckoningPositionsByUserView.as_view())#get info about reckoning positions that user has to pay


	#path('reckoningPositionMembers/<int:reckoningPosition_id>', ReckoningPositionMembersView.as_view()),	#get info about people present in reckoning position
]