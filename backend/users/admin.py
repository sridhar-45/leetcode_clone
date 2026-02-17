from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'problems_solved', 'ranking', 'date_joined']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile Information', {
            'fields': ('bio', 'avatar', 'location', 'website', 'github_username')
        }),
        ('Statistics', {
            'fields': ('problems_solved', 'easy_solved', 'medium_solved', 'hard_solved', 'ranking')
        }),
    )