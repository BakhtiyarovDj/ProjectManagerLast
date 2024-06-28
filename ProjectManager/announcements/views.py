from rest_framework.generics import *
from .models import Announcement, WorkRequest
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .permissions import IsCaptain, IsProjectManager


class AnnouncementListView(ListCreateAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Announcement.objects.filter(deleted_at__isnull=True)

class AnnouncementDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]






class WorkRequestListViewManager(ListCreateAPIView):
    permission_classes = [IsProjectManager]
    serializer_class = WorkRequestSerializer
    def get_queryset(self):
        return WorkRequest.objects.filter(deleted_at__isnull=True)


class WorkRequestListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkRequestSerializerWithOutAnn
    def get_queryset(self):
        return WorkRequest.objects.filter(deleted_at__isnull=True)


class DeletedWorkRequestListView(ListAPIView):
    serializer_class = WorkRequestSerializer
    #permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return WorkRequest.objects.filter(deleted_at__isnull=False)


class MyWorkRequestListView(ListCreateAPIView):
    serializer_class = WorkRequestSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['pk']
        return WorkRequest.objects.filter(requester=user_id, deleted_at__isnull=True)

class WorkRequestDetailView(RetrieveUpdateDestroyAPIView):
    queryset = WorkRequest.objects.all()
    serializer_class = WorkRequestSerializer
    #permission_classes = [IsAuthenticated, IsAdmin]

