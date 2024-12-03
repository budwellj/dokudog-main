# main_app/admin.py

from django.contrib import admin
from api.models import UserProfile, Theme, Language, Work

admin.site.register(UserProfile)
admin.site.register(Theme)
