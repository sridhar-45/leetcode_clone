"""
backend/submissions/serializers.py
Copy this into backend/submissions/serializers.py
"""
from rest_framework import serializers
from .models import Submission


class SubmissionSerializer(serializers.ModelSerializer):
    username      = serializers.CharField(source='user.username', read_only=True)
    problem_title = serializers.CharField(source='problem.title', read_only=True)
    problem_slug  = serializers.CharField(source='problem.slug', read_only=True)

    class Meta:
        model  = Submission
        fields = [
            'id', 'username', 'problem_title', 'problem_slug',
            'code', 'language', 'status',
            'runtime', 'memory',
            'test_cases_passed', 'test_cases_total',
            'points_earned', 'is_first_accepted',
            'error_message', 'test_results',
            'created_at',
        ]
        read_only_fields = [
            'id', 'username', 'problem_title', 'problem_slug',
            'status', 'runtime', 'memory',
            'test_cases_passed', 'test_cases_total',
            'points_earned', 'is_first_accepted',
            'error_message', 'test_results', 'created_at',
        ]


class SubmissionCreateSerializer(serializers.Serializer):
    """Used to RECEIVE a submission from the frontend"""
    problem_slug = serializers.SlugField()
    code         = serializers.CharField()
    language     = serializers.ChoiceField(choices=['python', 'javascript', 'java'])



