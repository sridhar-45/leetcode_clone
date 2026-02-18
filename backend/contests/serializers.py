"""
═══════════════════════════════════════════════════════════════
FILE: backend/contests/serializers.py
COPY ENTIRE CONTENT TO: backend/contests/serializers.py
═══════════════════════════════════════════════════════════════
"""
from rest_framework import serializers
from .models import Contest, ContestProblem, ContestParticipation, ContestSubmission
from problems.serializers import ProblemListSerializer
from users.serializers import PublicUserSerializer


class ContestProblemSerializer(serializers.ModelSerializer):
    problem = ProblemListSerializer(read_only=True)
    
    class Meta:
        model = ContestProblem
        fields = ['id', 'problem', 'order', 'points']


class ContestListSerializer(serializers.ModelSerializer):
    """Compact for contests list page"""
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    status = serializers.ReadOnlyField()
    
    class Meta:
        model = Contest
        fields = [
            'id', 'title', 'slug', 'is_official',
            'created_by_username', 'start_time', 'end_time',
            'duration_minutes', 'total_participants',
            'status', 'is_public',
        ]


class ContestDetailSerializer(serializers.ModelSerializer):
    """Full details for contest page"""
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    problems = ContestProblemSerializer(source='contest_problems', many=True, read_only=True)
    status = serializers.ReadOnlyField()
    time_until_start = serializers.ReadOnlyField()
    time_remaining = serializers.ReadOnlyField()
    
    class Meta:
        model = Contest
        fields = [
            'id', 'title', 'slug', 'description',
            'is_official', 'created_by', 'created_by_username',
            'join_code', 'is_public',
            'start_time', 'end_time', 'duration_minutes',
            'max_participants', 'min_participants', 'total_participants',
            'status', 'time_until_start', 'time_remaining',
            'problems', 'created_at',
        ]


class ContestCreateSerializer(serializers.ModelSerializer):
    """Create new contest"""
    problem_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=True
    )
    
    class Meta:
        model = Contest
        fields = [
            'title', 'description', 'start_time', 'end_time',
            'duration_minutes', 'is_public', 'max_participants',
            'min_participants', 'problem_ids',
        ]
    
    def create(self, validated_data):
        problem_ids = validated_data.pop('problem_ids')
        contest = Contest.objects.create(**validated_data)
        
        # Add problems
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
    user = PublicUserSerializer(read_only=True)
    
    class Meta:
        model = ContestParticipation
        fields = [
            'id', 'user', 'total_score', 'problems_solved',
            'rank', 'time_penalty', 'joined_at', 'last_submission_at',
        ]


