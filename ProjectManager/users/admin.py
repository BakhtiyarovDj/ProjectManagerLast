from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Team)
admin.site.register(Developer)
admin.site.register(SubTeam)