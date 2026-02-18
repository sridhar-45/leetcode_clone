"""
═══════════════════════════════════════════════════════════════
FILE: backend/groups/serializers.py
COPY ENTIRE CONTENT TO: backend/groups/serializers.py
═══════════════════════════════════════════════════════════════
"""
from rest_framework import serializers
from .models import Group, GroupMember, GroupInvitation
from users.serializers import PublicUserSerializer


class GroupMemberSerializer(serializers.ModelSerializer):
    user = PublicUserSerializer(read_only=True)
    is_admin = serializers.SerializerMethodField()
    
    class Meta:
        model = GroupMember
        fields = [
            'id', 'user', 'role', 'is_admin',
            'points_contributed', 'problems_solved', 'joined_at',
        ]
    
    def get_is_admin(self, obj):
        return obj.is_admin()


class GroupListSerializer(serializers.ModelSerializer):
    """Compact for groups list"""
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Group
        fields = [
            'id', 'name', 'slug', 'avatar',
            'created_by_username', 'current_members', 'max_members',
            'total_points', 'global_rank', 'is_active', 'is_public',
        ]


class GroupDetailSerializer(serializers.ModelSerializer):
    """Full details for group page"""
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    members = GroupMemberSerializer(many=True, read_only=True)
    is_member = serializers.SerializerMethodField()
    is_full = serializers.ReadOnlyField()
    
    class Meta:
        model = Group
        fields = [
            'id', 'name', 'slug', 'description', 'avatar',
            'created_by', 'created_by_username',
            'join_code', 'is_public',
            'max_members', 'current_members', 'is_full',
            'total_points', 'total_problems_solved',
            'contests_participated', 'contests_won', 'global_rank',
            'is_active', 'created_at', 'members', 'is_member',
        ]
    
    def get_is_member(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.members.filter(user=request.user).exists()
        return False


class GroupCreateSerializer(serializers.ModelSerializer):
    """Create new group"""
    
    class Meta:
        model = Group
        fields = ['name', 'description', 'avatar', 'is_public', 'max_members']


class GroupInvitationSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.name', read_only=True)
    invited_by_username = serializers.CharField(source='invited_by.username', read_only=True)
    invited_user_username = serializers.CharField(source='invited_user.username', read_only=True)
    
    class Meta:
        model = GroupInvitation
        fields = [
            'id', 'group', 'group_name',
            'invited_by', 'invited_by_username',
            'invited_user', 'invited_user_username',
            'message', 'status', 'sent_at', 'responded_at',
        ]


