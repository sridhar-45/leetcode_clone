"""
═══════════════════════════════════════════════════════════════
COMPLETE CONTEST SERIALIZERS
All serializers for individual and group contests
═══════════════════════════════════════════════════════════════

LOCATION: backend/contests/serializers.py
REPLACE YOUR ENTIRE FILE
"""

from rest_framework import serializers
from .models import (
    Contest, ContestProblem, ContestParticipation,
    ParticipantProblem, ContestSubmission, ContestNotification
)
from problems.serializers import ProblemListSerializer
from users.serializers import PublicUserSerializer


class ContestProblemSerializer(serializers.ModelSerializer):
    """Problems in a contest"""
    problem = ProblemListSerializer(read_only=True)
    problem_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = ContestProblem
        fields = ['id', 'problem', 'problem_id', 'order', 'points']


class ParticipantProblemSerializer(serializers.ModelSerializer):
    """Problems assigned to specific participant (UNIQUE_RANDOM mode)"""
    problem = ProblemListSerializer(read_only=True)
    
    class Meta:
        model = ParticipantProblem
        fields = [
            'id', 'problem', 'order', 'points',
            'is_solved', 'solved_at', 'attempts'
        ]


class ContestListSerializer(serializers.ModelSerializer):
    """Compact list view of contests"""
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    status = serializers.ReadOnlyField()
    contest_type_display = serializers.CharField(source='get_contest_type_display', read_only=True)
    assignment_mode_display = serializers.CharField(
        source='get_problem_assignment_mode_display', 
        read_only=True
    )
    
    class Meta:
        model = Contest
        fields = [
            'id', 'title', 'slug', 'description',
            'contest_type', 'contest_type_display',
            'created_by', 'created_by_username', 'is_official',
            'start_time', 'end_time', 'duration_minutes',
            'status', 'is_public', 'total_participants',
            'problem_assignment_mode', 'assignment_mode_display',
            'problems_count', 'is_recurring', 'recurrence_pattern',
            'created_at'
        ]


class ContestDetailSerializer(serializers.ModelSerializer):
    """Full detail view of contest"""
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    status = serializers.ReadOnlyField()
    time_until_start = serializers.ReadOnlyField()
    time_remaining = serializers.ReadOnlyField()
    contest_problems = ContestProblemSerializer(many=True, read_only=True)
    
    # Add participant's assigned problems if UNIQUE_RANDOM mode
    my_assigned_problems = serializers.SerializerMethodField()
    
    class Meta:
        model = Contest
        fields = [
            'id', 'title', 'slug', 'description',
            'contest_type', 'created_by', 'created_by_username', 'is_official',
            'start_time', 'end_time', 'duration_minutes',
            'join_code', 'invite_link', 'is_public',
            'max_participants', 'min_participants', 'total_participants',
            'problem_assignment_mode', 'problems_count',
            'send_notifications', 'notification_before_minutes',
            'is_recurring', 'recurrence_pattern',
            'status', 'time_until_start', 'time_remaining',
            'contest_problems', 'my_assigned_problems',
            'created_at', 'is_active'
        ]
    
    def get_my_assigned_problems(self, obj):
        """Get problems assigned to current user if UNIQUE_RANDOM mode"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return []
        
        if obj.problem_assignment_mode != 'UNIQUE_RANDOM':
            return []
        
        try:
            participation = obj.individual_participants.get(user=request.user)
            problems = participation.assigned_problems.all()
            return ParticipantProblemSerializer(problems, many=True).data
        except ContestParticipation.DoesNotExist:
            return []


class ContestCreateSerializer(serializers.ModelSerializer):
    """Create new contest"""
    problem_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        help_text="List of problem IDs (for SAME_FOR_ALL or MANUAL mode)"
    )
    
    class Meta:
        model = Contest
        fields = [
            'title', 'description', 'contest_type',
            'start_time', 'end_time', 'duration_minutes',
            'is_public', 'max_participants', 'min_participants',
            'problem_assignment_mode', 'problems_count',
            'send_notifications', 'notification_before_minutes',
            'is_recurring', 'recurrence_pattern',
            'problem_ids'
        ]
    
    def validate(self, data):
        """Validate contest data"""
        # If SAME_FOR_ALL or MANUAL, problem_ids required
        if data.get('problem_assignment_mode') in ['SAME_FOR_ALL', 'MANUAL']:
            if not data.get('problem_ids'):
                raise serializers.ValidationError({
                    'problem_ids': 'Problem IDs required for this assignment mode'
                })
        
        # Validate dates
        if data['end_time'] <= data['start_time']:
            raise serializers.ValidationError({
                'end_time': 'End time must be after start time'
            })
        
        return data
    
    def create(self, validated_data):
        """Create contest and assign problems"""
        problem_ids = validated_data.pop('problem_ids', [])
        
        contest = Contest.objects.create(**validated_data)
        
        # Add problems if provided
        if problem_ids and contest.problem_assignment_mode in ['SAME_FOR_ALL', 'MANUAL']:
            from problems.models import Problem
            for idx, pid in enumerate(problem_ids):
                try:
                    problem = Problem.objects.get(id=pid)
                    ContestProblem.objects.create(
                        contest=contest,
                        problem=problem,
                        order=idx,
                        points=problem.points
                    )
                except Problem.DoesNotExist:
                    pass
        
        return contest


class ContestParticipationSerializer(serializers.ModelSerializer):
    """Participant in contest"""
    user = PublicUserSerializer(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = ContestParticipation
        fields = [
            'id', 'user', 'username',
            'total_score', 'problems_solved', 'rank',
            'time_penalty', 'joined_at', 'last_submission_at'
        ]


class ContestSubmissionSerializer(serializers.ModelSerializer):
    """Submission in contest"""
    username = serializers.CharField(source='participant.user.username', read_only=True)
    problem_title = serializers.CharField(source='problem.title', read_only=True)
    
    class Meta:
        model = ContestSubmission
        fields = [
            'id', 'username', 'problem_title',
            'points_earned', 'time_from_start',
            'created_at'
        ]


class ContestNotificationSerializer(serializers.ModelSerializer):
    """Contest notification"""
    contest_title = serializers.CharField(source='contest.title', read_only=True)
    
    class Meta:
        model = ContestNotification
        fields = [
            'id', 'contest', 'contest_title',
            'notification_type', 'message',
            'sent_at', 'is_read', 'read_at'
        ]


class JoinContestSerializer(serializers.Serializer):
    """Data for joining a contest"""
    join_code = serializers.CharField(required=False, allow_blank=True)