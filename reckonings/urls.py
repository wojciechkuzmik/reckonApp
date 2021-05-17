from django.urls import path
from .views import CreateReckoningView,ReckoningView,CreateReckoningPositionView,CreateCategoryView, ReckoningPositionsView,CategoriesView, CategoryView, ReckoningsInGroupView, ReckoningPositionsForUserView,ReckoningPositionsByUserView
#ReckoningPositionMembersView

urlpatterns = [
	path('category', CreateCategoryView.as_view()),	#create category
	path('categories',CategoriesView.as_view()),#show all categories
	path('category/<int:cat_id>',CategoryView.as_view()),#show one category 
	path('reckoning', CreateReckoningView.as_view()),	#create reckoning
	path('reckoning/<int:reckoning_id>',ReckoningView.as_view()),#get info about reckoning 
	path('reckonings_in_group/<int:group_id>',ReckoningsInGroupView.as_view()),#get info about reckonings in group
	path('reckoningPosition', CreateReckoningPositionView.as_view()),	#create reckoningPosition
	path('reckoningPosition/<int:reckoning_id>', ReckoningPositionsView.as_view()),	#get info about reckoning positions in reckoning
	path('reckoningPositionsForUser/<int:user_id>',ReckoningPositionsForUserView.as_view()),#get info about reckoning positions that user has to pay
	path('reckoningPositionsByUser/<int:user_id>',ReckoningPositionsByUserView.as_view())#get info about reckoning positions that user has to pay


	#path('reckoningPositionMembers/<int:reckoningPosition_id>', ReckoningPositionMembersView.as_view()),	#get info about people present in reckoning position
]