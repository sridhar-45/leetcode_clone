"""
═══════════════════════════════════════════════════════════════
FILE: backend/contests/admin.py
COPY ENTIRE CONTENT TO: backend/contests/admin.py
═══════════════════════════════════════════════════════════════
"""
from django.contrib import admin
from .models import Contest, ContestProblem, ContestParticipation


class ContestProblemInline(admin.TabularInline):
    model = ContestProblem
    extra = 1


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_official', 'start_time', 'status', 'total_participants']
    list_filter = ['is_official', 'is_public', 'start_time']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ContestProblemInline]


@admin.register(ContestParticipation)
class ContestParticipationAdmin(admin.ModelAdmin):
    list_display = ['contest', 'user', 'rank', 'total_score', 'problems_solved']
    list_filter = ['contest']
    search_fields = ['user__username', 'contest__title']