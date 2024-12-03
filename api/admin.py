from django.contrib import admin
from .models import UserProfile, Theme, Language, Type, Work
# Register your models here.
# Register your models here
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'difficulty_score', 'native_language', 'target_language')
    search_fields = ('user__username',)

@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'difficulty', 'type', 'language')
    list_filter = ('type', 'language', 'difficulty')
    search_fields = ('title', 'author')
    filter_horizontal = ('themes',)