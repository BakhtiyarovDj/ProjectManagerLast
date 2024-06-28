from django.urls import path
from .views import *

urlpatterns = [
    path('', AnnouncementListView.as_view()),
    path('<int:pk>/', AnnouncementDetailView.as_view(), name='announcement-detail'),
    path('requests/for-manager/', WorkRequestListViewManager.as_view()),
    path('requests/', WorkRequestListView.as_view()),
    path('myrequests/captain/<int:pk>', MyWorkRequestListView.as_view()),
    path('requests/deleted/', DeletedWorkRequestListView.as_view()), 
    path('requests/<int:pk>/', WorkRequestDetailView.as_view(), name='workrequest-detail'),

]