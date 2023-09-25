from django.urls import path
from .views import OnlineUsersView

urlpatterns = [
    path('api/online-users', OnlineUsersView.as_view())
]