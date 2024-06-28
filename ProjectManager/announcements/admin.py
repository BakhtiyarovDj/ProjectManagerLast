from django.contrib import admin
from .models import Announcement, Document, WorkRequest


# @admin.register(Announcement)
# class RoomAdmin(admin.ModelAdmin):

#     list_display = (
#         "project_name",
#         "cost",
#     )


# @admin.register(Document)
# class RoomAdmin(admin.ModelAdmin):

#     list_display = (
#         "announcement",
#     )

# @admin.register(WorkRequest)
# class RoomAdmin(admin.ModelAdmin):

#     list_display = (
#         "id",
#         "announcement",
#         "requester",
#     )