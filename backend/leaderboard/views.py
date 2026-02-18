"""
═══════════════════════════════════════════════════════════════
FILE: backend/leaderboard/views.py
COPY ENTIRE CONTENT TO: backend/leaderboard/views.py
═══════════════════════════════════════════════════════════════
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from users.models import User
from groups.models import Group
from users.serializers import PublicUserSerializer
from groups.serializers import GroupListSerializer


class GlobalLeaderboardView(APIView):
    """GET /api/leaderboard/global/ - Top users"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        limit = int(request.query_params.get('limit', 100))
        
        top_users = User.objects.filter(
            is_active=True
        ).order_by('-total_points', '-problems_solved')[:limit]
        
        serializer = PublicUserSerializer(top_users, many=True)
        
        return Response({
            'count': top_users.count(),
            'leaderboard': serializer.data,
        })


class GroupLeaderboardView(APIView):
    """GET /api/leaderboard/groups/ - Top groups"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        limit = int(request.query_params.get('limit', 100))
        
        top_groups = Group.objects.filter(
            is_active=True
        ).order_by('-total_points', '-total_problems_solved')[:limit]
        
        serializer = GroupListSerializer(top_groups, many=True)
        
        return Response({
            'count': top_groups.count(),
            'leaderboard': serializer.data,
        })


