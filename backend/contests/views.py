"""
═══════════════════════════════════════════════════════════════
COMPLETE CONTEST VIEWS
All API endpoints with complete logic
═══════════════════════════════════════════════════════════════

LOCATION: backend/contests/views.py
REPLACE YOUR ENTIRE FILE
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from .models import (
    Contest, ContestParticipation, ContestNotification,
    ParticipantProblem
)
from .serializers import (
    ContestListSerializer, ContestDetailSerializer,
    ContestCreateSerializer, ContestParticipationSerializer,
    JoinContestSerializer, ParticipantProblemSerializer,
    ContestNotificationSerializer
)


class ContestListView(generics.ListAPIView):
    """
    GET /api/contests/
    List all contests with filters
    
    Query Parameters:
    - type: 'INDIVIDUAL' or 'GROUP'
    - status: 'live', 'upcoming', 'past'
    - recurring: 'true' or 'false'
    """
    serializer_class = ContestListSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        qs = Contest.objects.filter(is_active=True).order_by('-start_time')
        
        # Filter by contest type
        contest_type = self.request.query_params.get('type')
        if contest_type:
            qs = qs.filter(contest_type=contest_type)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        now = timezone.now()
        
        if status_filter == 'live':
            qs = qs.filter(start_time__lte=now, end_time__gte=now)
        elif status_filter == 'upcoming':
            qs = qs.filter(start_time__gt=now)
        elif status_filter == 'past':
            qs = qs.filter(end_time__lt=now)
        
        # Filter by recurring
        recurring = self.request.query_params.get('recurring')
        if recurring == 'true':
            qs = qs.filter(is_recurring=True)
        elif recurring == 'false':
            qs = qs.filter(is_recurring=False)
        
        return qs


class ContestDetailView(generics.RetrieveAPIView):
    """
    GET /api/contests/<slug>/
    Get contest details
    
    Returns:
    - Contest info
    - Problems (if SAME_FOR_ALL or MANUAL mode)
    - User's assigned problems (if UNIQUE_RANDOM mode and user joined)
    """
    serializer_class = ContestDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'
    queryset = Contest.objects.filter(is_active=True)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class ContestCreateView(APIView):
    """
    POST /api/contests/create/
    Create new contest
    
    Body:
    {
        "title": "Weekly Challenge",
        "contest_type": "INDIVIDUAL",
        "problem_assignment_mode": "SAME_FOR_ALL",
        "problems_count": 5,
        "problem_ids": [1, 2, 3, 4, 5],  // If SAME_FOR_ALL or MANUAL
        "start_time": "2026-03-25T10:00:00Z",
        "end_time": "2026-03-25T12:00:00Z",
        "duration_minutes": 120,
        "is_public": true,
        "send_notifications": true,
        "is_recurring": false
    }
    
    Returns:
    - Created contest with join_code and invite_link
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ContestCreateSerializer(data=request.data)
        if serializer.is_valid():
            contest = serializer.save(created_by=request.user)
            
            return Response(
                ContestDetailSerializer(contest, context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContestJoinView(APIView):
    """
    POST /api/contests/<slug>/join/
    Join a contest
    
    Body (for private contests):
    {
        "join_code": "ABC12XYZ"
    }
    
    Logic:
    1. Check if user already joined
    2. Validate join code (if private)
    3. Create ContestParticipation
    4. Assign problems based on mode:
       - SAME_FOR_ALL: No action (uses ContestProblem)
       - UNIQUE_RANDOM: Assign random unique problems
       - MANUAL: No action (uses ContestProblem)
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @transaction.atomic
    def post(self, request, slug):
        contest = get_object_or_404(Contest, slug=slug, is_active=True)
        
        # Check if contest is for individuals only
        if contest.contest_type != 'INDIVIDUAL':
            return Response(
                {'error': 'This contest is for groups only.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if already joined
        if contest.individual_participants.filter(user=request.user).exists():
            return Response(
                {'error': 'You have already joined this contest.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate join code for private contests
        if not contest.is_public:
            serializer = JoinContestSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            join_code = serializer.validated_data.get('join_code', '')
            if join_code != contest.join_code:
                return Response(
                    {'error': 'Invalid join code.'},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        # Check participant limit
        if contest.total_participants >= contest.max_participants:
            return Response(
                {'error': 'Contest is full.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create participation
        participation = ContestParticipation.objects.create(
            contest=contest,
            user=request.user
        )
        
        # Assign problems based on mode
        try:
            contest.assign_problems_to_participant(participation)
        except ValueError as e:
            participation.delete()
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({
            'message': 'Successfully joined contest!',
            'participation': ContestParticipationSerializer(participation).data,
            'join_code': contest.join_code,
            'invite_link': f"{request.scheme}://{request.get_host()}/contests/join/{contest.invite_link}"
        })


class ContestJoinByLinkView(APIView):
    """
    GET /api/contests/join/<invite_link>/
    Join contest via invite link
    
    Logic:
    - Same as regular join but uses invite_link instead of slug
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, invite_link):
        contest = get_object_or_404(Contest, invite_link=invite_link, is_active=True)
        
        # Use regular join logic
        view = ContestJoinView()
        view.request = request
        return view.post(request, contest.slug)


class ContestLeaderboardView(APIView):
    """
    GET /api/contests/<slug>/leaderboard/
    Get contest leaderboard
    
    Logic:
    1. Recalculate scores for all participants
    2. Update ranks
    3. Return sorted leaderboard
    
    Returns:
    - Sorted list of participants with scores and ranks
    """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, slug):
        contest = get_object_or_404(Contest, slug=slug, is_active=True)
        
        if contest.contest_type != 'INDIVIDUAL':
            return Response(
                {'error': 'Use group contest leaderboard endpoint.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Recalculate scores
        for participant in contest.individual_participants.all():
            participant.calculate_score()
        
        # Update ranks
        participants = contest.individual_participants.all().order_by('-total_score', 'time_penalty')
        for rank, participant in enumerate(participants, start=1):
            participant.rank = rank
            participant.save(update_fields=['rank'])
        
        serializer = ContestParticipationSerializer(participants, many=True)
        
        return Response({
            'contest': ContestListSerializer(contest).data,
            'leaderboard': serializer.data,
        })


class MyContestsView(APIView):
    """
    GET /api/contests/my/
    Get contests user is participating in
    
    Returns:
    - List of contests user joined
    - Including past, live, and upcoming
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        participations = ContestParticipation.objects.filter(
            user=request.user
        ).select_related('contest')
        
        contests = [p.contest for p in participations if p.contest.is_active]
        serializer = ContestListSerializer(contests, many=True)
        
        return Response({
            'count': len(contests),
            'contests': serializer.data,
        })


class MyCreatedContestsView(APIView):
    """
    GET /api/contests/created/
    Get contests created by user
    
    Returns:
    - Contests user created
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        contests = Contest.objects.filter(
            created_by=request.user,
            is_active=True
        ).order_by('-created_at')
        
        serializer = ContestListSerializer(contests, many=True)
        return Response(serializer.data)


class MyAssignedProblemsView(APIView):
    """
    GET /api/contests/<slug>/my-problems/
    Get problems assigned to current user
    
    Used for UNIQUE_RANDOM mode
    
    Returns:
    - List of problems assigned to this user
    - Progress on each problem
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, slug):
        contest = get_object_or_404(Contest, slug=slug, is_active=True)
        
        # Get user's participation
        try:
            participation = contest.individual_participants.get(user=request.user)
        except ContestParticipation.DoesNotExist:
            return Response(
                {'error': 'You have not joined this contest.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get assigned problems
        if contest.problem_assignment_mode == 'UNIQUE_RANDOM':
            problems = participation.assigned_problems.all()
            serializer = ParticipantProblemSerializer(problems, many=True)
        else:
            # Use common problems
            from .serializers import ContestProblemSerializer
            problems = contest.contest_problems.all()
            serializer = ContestProblemSerializer(problems, many=True)
        
        return Response({
            'contest': ContestListSerializer(contest).data,
            'problems': serializer.data,
            'assignment_mode': contest.problem_assignment_mode,
        })


class MyNotificationsView(APIView):
    """
    GET /api/contests/notifications/
    Get user's contest notifications
    
    Returns:
    - List of notifications
    - Unread count
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        notifications = ContestNotification.objects.filter(
            user=request.user
        ).order_by('-sent_at')
        
        unread_count = notifications.filter(is_read=False).count()
        
        serializer = ContestNotificationSerializer(notifications, many=True)
        
        return Response({
            'notifications': serializer.data,
            'unread_count': unread_count,
        })


class MarkNotificationReadView(APIView):
    """
    POST /api/contests/notifications/<id>/read/
    Mark notification as read
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, notification_id):
        notification = get_object_or_404(
            ContestNotification,
            id=notification_id,
            user=request.user
        )
        
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()
        
        return Response({'message': 'Notification marked as read'})


class ContestProblemsView(APIView):
    """
    GET /api/contests/<slug>/problems/
    Get all problems in contest (for SAME_FOR_ALL mode)
    
    Returns:
    - List of problems everyone gets
    """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, slug):
        contest = get_object_or_404(Contest, slug=slug, is_active=True)
        
        if contest.problem_assignment_mode == 'UNIQUE_RANDOM':
            return Response(
                {'error': 'This contest has unique problems per participant. Use /my-problems/ endpoint.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from .serializers import ContestProblemSerializer
        problems = contest.contest_problems.all()
        serializer = ContestProblemSerializer(problems, many=True)
        
        return Response({
            'contest': ContestListSerializer(contest).data,
            'problems': serializer.data,
        })


"""
═══════════════════════════════════════════════════════════════
COMPLETE API ENDPOINT SUMMARY
═══════════════════════════════════════════════════════════════

PUBLIC ENDPOINTS (No authentication required):
──────────────────────────────────────────────
GET    /api/contests/                         - List all contests
GET    /api/contests/<slug>/                   - Contest details
GET    /api/contests/<slug>/leaderboard/       - Leaderboard
GET    /api/contests/<slug>/problems/          - Contest problems (SAME_FOR_ALL mode)

AUTHENTICATED ENDPOINTS (Login required):
─────────────────────────────────────────
POST   /api/contests/create/                   - Create contest
POST   /api/contests/<slug>/join/              - Join contest
GET    /api/contests/join/<invite_link>/       - Join via invite link
GET    /api/contests/my/                       - My participations
GET    /api/contests/created/                  - Contests I created
GET    /api/contests/<slug>/my-problems/       - My assigned problems
GET    /api/contests/notifications/            - My notifications
POST   /api/contests/notifications/<id>/read/  - Mark notification read


WORKFLOW EXAMPLES:
─────────────────

1. CREATE CONTEST (SAME PROBLEMS FOR ALL):
   POST /api/contests/create/
   {
       "title": "Weekly Challenge",
       "contest_type": "INDIVIDUAL",
       "problem_assignment_mode": "SAME_FOR_ALL",
       "problem_ids": [1, 2, 3, 4, 5],
       "start_time": "2026-03-25T10:00:00Z",
       ...
   }
   
   Response: Contest created with join_code and invite_link

2. CREATE CONTEST (UNIQUE RANDOM PROBLEMS):
   POST /api/contests/create/
   {
       "title": "Random Challenge",
       "contest_type": "INDIVIDUAL",
       "problem_assignment_mode": "UNIQUE_RANDOM",
       "problems_count": 7,
       ...
   }
   
   Response: Contest created (no problem_ids needed!)

3. JOIN CONTEST:
   POST /api/contests/weekly-challenge-abc123/join/
   
   If SAME_FOR_ALL: User gets same 5 problems as everyone
   If UNIQUE_RANDOM: User gets 7 random problems assigned

4. VIEW MY PROBLEMS:
   GET /api/contests/weekly-challenge-abc123/my-problems/
   
   Returns: User's specific assigned problems

5. VIEW LEADERBOARD:
   GET /api/contests/weekly-challenge-abc123/leaderboard/
   
   Returns: Sorted participants with scores

6. SHARE INVITE:
   Share: https://yoursite.com/contests/join/contest-xyz123abc456
   
   Friend clicks → Auto-joins contest
"""