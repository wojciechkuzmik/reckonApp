from django.urls import path
from .views import CreateReckoningView,ReckoningView,CreateReckoningPositionView,CreateCategoryView, ReckoningPositionsView
#ReckoningPositionMembersView

urlpatterns = [
	path('category', CreateCategoryView.as_view()),	#create category
	path('reckoning', CreateReckoningView.as_view()),	#create reckoning
	path('reckoning/<int:reckoning_id>',ReckoningView.as_view()),#get info about reckoning 
	path('reckoningPosition', CreateReckoningPositionView.as_view()),	#create reckoningPosition
	path('reckoningPosition/<int:reckoning_id>', ReckoningPositionsView.as_view()),	#get info about reckoning positions in reckoning
	#path('reckoningPositionMembers/<int:reckoningPosition_id>', ReckoningPositionMembersView.as_view()),	#get info about people present in reckoning position
]