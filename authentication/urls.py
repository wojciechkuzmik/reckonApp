from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView, SearchView

urlpatterns = [
	path('register', RegisterView.as_view()),
	path('login', LoginView.as_view()),
	path('logged', UserView.as_view()),
	path('logout', LogoutView.as_view()),
	path('search', SearchView.as_view())
]