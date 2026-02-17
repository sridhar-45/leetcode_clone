"""
backend/users/admin.py
FIXED - Removed 'ranking' which doesn't exist, use 'global_ranking' instead
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, DailyProblem, DailyProblemCompletion


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # FIXED: Changed 'ranking' to 'global_ranking'
    list_display = [
        'username',
        'email',
        'problems_solved',
        'total_points',
        'global_ranking',      # ← FIXED (was 'ranking')
        'current_streak',
        'is_staff',
        'date_joined',
    ]

    list_filter = [
        'is_staff',
        'is_superuser',
        'is_active',
        'date_joined',
    ]

    search_fields = [
        'username',
        'email',
        'first_name',
        'last_name',
    ]

    ordering = ['-total_points']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile Information', {
            'fields': (
                'bio', 'avatar', 'location',
                'website', 'github_username'
            )
        }),
        ('Problem Statistics', {
            'fields': (
                'problems_solved',
                'easy_solved',
                'medium_solved',
                'hard_solved',
            )
        }),
        ('Points & Ranking', {
            'fields': (
                'total_points',
                'global_ranking',
            )
        }),
        ('Streak Information', {
            'fields': (
                'current_streak',
                'longest_streak',
                'last_activity_date',
            )
        }),
        ('Contest Stats', {
            'fields': (
                'contests_participated',
                'contests_won',
            )
        }),
    )


@admin.register(DailyProblem)
class DailyProblemAdmin(admin.ModelAdmin):
    list_display = ['date', 'problem', 'created_at']
    ordering = ['-date']


@admin.register(DailyProblemCompletion)
class DailyProblemCompletionAdmin(admin.ModelAdmin):
    list_display = ['user', 'daily_problem', 'completed_at']
    list_filter = ['daily_problem__date']
    ordering = ['-completed_at']