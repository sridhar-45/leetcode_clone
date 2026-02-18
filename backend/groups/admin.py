"""
═══════════════════════════════════════════════════════════════
FILE: backend/groups/admin.py
COPY ENTIRE CONTENT TO: backend/groups/admin.py
═══════════════════════════════════════════════════════════════
"""
from django.contrib import admin
from .models import Group, GroupMember, GroupInvitation


class GroupMemberInline(admin.TabularInline):
    model = GroupMember
    extra = 0


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'current_members', 'total_points', 'global_rank', 'is_active']
    list_filter = ['is_active', 'is_public']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [GroupMemberInline]


@admin.register(GroupInvitation)
class GroupInvitationAdmin(admin.ModelAdmin):
    list_display = ['group', 'invited_user', 'status', 'sent_at']
    list_filter = ['status']