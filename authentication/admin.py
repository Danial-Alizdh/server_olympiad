# user_management/admin.py
from django.contrib import admin
from .models import *

admin.site.register(DepartmentNews)
admin.site.register(UserProfile)
admin.site.register(Coach)
admin.site.register(GymManager)
admin.site.register(Actor)
admin.site.register(Office)
admin.site.register(OfficeAuthorities)
admin.site.register(Board)
admin.site.register(BoardAuthorities)
admin.site.register(BoardGame)
admin.site.register(Classroom)
admin.site.register(JoinedClass)
admin.site.register(Message)
