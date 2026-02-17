from rest_framework import serializers
from .models import Problem, TestCase, Topic, Tag


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name', 'slug']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ['id', 'input_data', 'expected_output', 'explanation', 'order']


class ProblemListSerializer(serializers.ModelSerializer):
    """Compact serializer for problem list page"""
    topics = TopicSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Problem
        fields = [
            'id', 'title', 'slug', 'difficulty', 'points',
            'acceptance_rate', 'total_submissions',
            'topics', 'tags', 'is_premium',
        ]


class ProblemDetailSerializer(serializers.ModelSerializer):
    """Full serializer for problem detail page"""
    topics = TopicSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    test_cases = serializers.SerializerMethodField()

    class Meta:
        model = Problem
        fields = [
            'id', 'title', 'slug', 'description',
            'difficulty', 'points', 'constraints', 'examples',
            'hints', 'template_python', 'template_javascript',
            'template_java', 'topics', 'tags',
            'acceptance_rate', 'total_submissions',
            'is_premium', 'test_cases',
        ]

    def get_test_cases(self, obj):
        """Only return PUBLIC test cases"""
        public_cases = obj.test_cases.filter(is_public=True)
        return TestCaseSerializer(public_cases, many=True).data