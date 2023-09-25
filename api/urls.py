from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView, FriendsRecommendationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('login/',  UserLoginView.as_view()),
    path('logout/',  UserLogoutView.as_view()),
    path('suggested-friends/<int:user_id>/', FriendsRecommendationView.as_view())
]