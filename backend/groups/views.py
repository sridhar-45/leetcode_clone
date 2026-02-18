"""
═══════════════════════════════════════════════════════════════
FILE: backend/groups/views.py
COPY ENTIRE CONTENT TO: backend/groups/views.py
═══════════════════════════════════════════════════════════════
"""
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.text import slugify
from .models import Group, GroupMember, GroupInvitation
from .serializers import (
    GroupListSerializer, GroupDetailSerializer,
    GroupCreateSerializer, GroupMemberSerializer,
    GroupInvitationSerializer
)


class GroupListView(generics.ListAPIView):
    """GET /api/groups/ - All groups"""
    serializer_class = GroupListSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        qs = Group.objects.filter(is_active=True).order_by('-total_points')
        
        # Filter by public/private
        visibility = self.request.query_params.get('visibility')
        if visibility == 'public':
            qs = qs.filter(is_public=True)
        
        # Search
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(name__icontains=search)
        
        return qs


class GroupDetailView(generics.RetrieveAPIView):
    """GET /api/groups/<slug>/ - Group details"""
    serializer_class = GroupDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'
    queryset = Group.objects.filter(is_active=True)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class GroupCreateView(APIView):
    """POST /api/groups/create/ - Create new group"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = GroupCreateSerializer(data=request.data)
        if serializer.is_valid():
            group = serializer.save(created_by=request.user)
            group.slug = slugify(group.name) + f'-{group.id}'
            group.save()
            
            # Creator becomes admin member
            GroupMember.objects.create(
                group=group,
                user=request.user,
                role='ADMIN'
            )
            
            return Response(
                GroupDetailSerializer(group, context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupJoinView(APIView):
    """POST /api/groups/<slug>/join/ - Join a group"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, slug):
        try:
            group = Group.objects.get(slug=slug, is_active=True)
        except Group.DoesNotExist:
            return Response({'error': 'Group not found.'}, status=404)
        
        # Check join code for private groups
        if not group.is_public:
            join_code = request.data.get('join_code', '')
            if join_code != group.join_code:
                return Response({'error': 'Invalid join code.'}, status=403)
        
        success, message = group.add_member(request.user)
        if success:
            return Response({'message': message})
        return Response({'error': message}, status=400)


class GroupLeaveView(APIView):
    """POST /api/groups/<slug>/leave/ - Leave group"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, slug):
        try:
            group = Group.objects.get(slug=slug, is_active=True)
        except Group.DoesNotExist:
            return Response({'error': 'Group not found.'}, status=404)
        
        # Can't leave if you're the creator
        if group.created_by == request.user:
            return Response(
                {'error': 'Group creator cannot leave. Delete the group instead.'},
                status=400
            )
        
        success, message = group.remove_member(request.user)
        if success:
            return Response({'message': message})
        return Response({'error': message}, status=400)


class GroupMembersView(APIView):
    """GET /api/groups/<slug>/members/ - Group members list"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, slug):
        try:
            group = Group.objects.get(slug=slug, is_active=True)
        except Group.DoesNotExist:
            return Response({'error': 'Group not found.'}, status=404)
        
        members = group.members.select_related('user').order_by('-points_contributed')
        serializer = GroupMemberSerializer(members, many=True)
        
        return Response({
            'group': GroupListSerializer(group).data,
            'members': serializer.data,
        })


class MyGroupsView(APIView):
    """GET /api/groups/my/ - User's groups"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        memberships = GroupMember.objects.filter(
            user=request.user
        ).select_related('group')
        
        groups = [m.group for m in memberships if m.group.is_active]
        serializer = GroupListSerializer(groups, many=True)
        
        return Response({
            'count': len(groups),
            'groups': serializer.data,
        })


class GroupInviteView(APIView):
    """POST /api/groups/<slug>/invite/ - Invite user to group"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, slug):
        try:
            group = Group.objects.get(slug=slug, is_active=True)
        except Group.DoesNotExist:
            return Response({'error': 'Group not found.'}, status=404)
        
        # Check if requester is admin
        try:
            membership = group.members.get(user=request.user)
            if not membership.is_admin():
                return Response({'error': 'Only admins can invite.'}, status=403)
        except GroupMember.DoesNotExist:
            return Response({'error': 'You are not a member.'}, status=403)
        
        # Get user to invite
        from users.models import User
        username = request.data.get('username')
        try:
            invited_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)
        
        # Create invitation
        invitation, created = GroupInvitation.objects.get_or_create(
            group=group,
            invited_user=invited_user,
            defaults={
                'invited_by': request.user,
                'message': request.data.get('message', ''),
            }
        )
        
        if not created:
            return Response({'error': 'Invitation already sent.'}, status=400)
        
        return Response(
            GroupInvitationSerializer(invitation).data,
            status=status.HTTP_201_CREATED
        )

