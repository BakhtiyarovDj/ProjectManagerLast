from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('api/userinfo/', UserInfoView.as_view(), name='userinfo'),
    path('teamlist/', TeamCreateAPIView.as_view()),
    path('teamlist/create', create_team_user, name='create_team_user'),
    path('teamlist/<int:pk>', TeamDetailView.as_view(), name='team-detail'),
    path('teamlist/with-user/<int:pk>/', TeamWithUserIDView.as_view()),
    path('userlist/',UserCreateAPIView.as_view()),
    path('userlist/<int:pk>', UserDetailView.as_view(), name='user-detail'),
    path('subteamlist/', SubTeamCreateAPIView.as_view()),
    path('subteamlist/<int:pk>', SubTeamDetailView.as_view(), name='subteam-detail'),
    path('subteamlist/with-team/<int:pk>', SubTeamWithTeamView.as_view(), name='subteam-detail'),
    path('developer/', DeveloperCreateAPIView.as_view(), name='developer'),
    path('developer/<int:pk>', DeveloperDetailView.as_view(), name='developer-detail'),
    path('developer/<str:teamtitle>/<int:pk>', DevelopersFromTeamAPIView.as_view()),

    path('getteamdatafromuser/<int:pk>/', GetTeamFromUserIDView.as_view()), 

    path('employment/', EmploymentAPIView.as_view()), 

    path('employment/<int:teamid>', EmploymentChangeAPIView.as_view()), 

] 