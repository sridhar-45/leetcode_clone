"""
═══════════════════════════════════════════════════════════════
FILE: backend/contests/views.py
COPY ENTIRE CONTENT TO: backend/contests/views.py
═══════════════════════════════════════════════════════════════
"""
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.text import slugify
from django.utils import timezone
from .models import Contest, ContestParticipation
from .serializers import (
    ContestListSerializer, ContestDetailSerializer,
    ContestCreateSerializer, ContestParticipationSerializer
)


class ContestListView(generics.ListAPIView):
    """GET /api/contests/ - All contests"""
    serializer_class = ContestListSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        qs = Contest.objects.all().order_by('-start_time')
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter == 'live':
            now = timezone.now()
            qs = qs.filter(start_time__lte=now, end_time__gte=now)
        elif status_filter == 'upcoming':
            qs = qs.filter(start_time__gt=timezone.now())
        elif status_filter == 'past':
            qs = qs.filter(end_time__lt=timezone.now())
        
        # Filter by type
        contest_type = self.request.query_params.get('type')
        if contest_type == 'official':
            qs = qs.filter(is_official=True)
        elif contest_type == 'community':
            qs = qs.filter(is_official=False)
        
        return qs


class ContestDetailView(generics.RetrieveAPIView):
    """GET /api/contests/<slug>/ - Contest details"""
    serializer_class = ContestDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'
    queryset = Contest.objects.all()


class ContestCreateView(APIView):
    """POST /api/contests/create/ - Create new contest"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ContestCreateSerializer(data=request.data)
        if serializer.is_valid():
            contest = serializer.save(created_by=request.user)
            contest.slug = slugify(contest.title) + f'-{contest.id}'
            contest.save()
            
            return Response(
                ContestDetailSerializer(contest).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContestJoinView(APIView):
    """POST /api/contests/<slug>/join/ - Join a contest"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, slug):
        try:
            contest = Contest.objects.get(slug=slug)
        except Contest.DoesNotExist:
            return Response({'error': 'Contest not found.'}, status=404)
        
        # Check join code for private contests
        if not contest.is_public:
            join_code = request.data.get('join_code', '')
            if join_code != contest.join_code:
                return Response({'error': 'Invalid join code.'}, status=403)
        
        success, message = contest.join_contest(request.user)
        if success:
            participation = contest.participants.get(user=request.user)
            return Response({
                'message': message,
                'participation': ContestParticipationSerializer(participation).data,
            })
        return Response({'error': message}, status=400)


class ContestLeaderboardView(APIView):
    """GET /api/contests/<slug>/leaderboard/ - Contest rankings"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, slug):
        try:
            contest = Contest.objects.get(slug=slug)
        except Contest.DoesNotExist:
            return Response({'error': 'Contest not found.'}, status=404)
        
        leaderboard = contest.get_leaderboard()
        serializer = ContestParticipationSerializer(leaderboard, many=True)
        
        return Response({
            'contest': ContestListSerializer(contest).data,
            'leaderboard': serializer.data,
        })


class MyContestsView(APIView):
    """GET /api/contests/my/ - User's contests"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Contests user is participating in
        participations = ContestParticipation.objects.filter(
            user=request.user
        ).select_related('contest')
        
        contests = [p.contest for p in participations]
        serializer = ContestListSerializer(contests, many=True)
        
        return Response({
            'count': len(contests),
            'contests': serializer.data,
        })


class MyCreatedContestsView(APIView):
    """GET /api/contests/created/ - Contests user created"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        contests = Contest.objects.filter(created_by=request.user)
        serializer = ContestListSerializer(contests, many=True)
        return Response(serializer.data)

