# user_management/admin.py
from django.contrib import admin
from .models import *

admin.site.register(DepartmentNews)
admin.site.register(UserProfile)
admin.site.register(Coach)
admin.site.register(GymManager)
admin.site.register(Actor)
