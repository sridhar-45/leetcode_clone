from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Problem, Topic, Tag
from .serializers import (
    ProblemListSerializer, ProblemDetailSerializer,
    TopicSerializer, TagSerializer
)


class ProblemListView(generics.ListAPIView):
    """
    GET /api/problems/
    List all problems with optional filters.
    Supports: ?difficulty=EASY&topic=arrays&search=two+sum
    """
    serializer_class = ProblemListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['id', 'difficulty', 'acceptance_rate', 'total_submissions']
    ordering = ['id']

    def get_queryset(self):
        queryset = Problem.objects.filter(is_active=True)

        # Filter by difficulty
        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty.upper())

        # Filter by topic
        topic = self.request.query_params.get('topic')
        if topic:
            queryset = queryset.filter(topics__slug=topic)

        # Filter by status (solved/unsolved for logged-in users)
        status_filter = self.request.query_params.get('status')
        if status_filter and self.request.user.is_authenticated:
            from submissions.models import Submission
            solved_ids = Submission.objects.filter(
                user=self.request.user,
                status='ACCEPTED'
            ).values_list('problem_id', flat=True).distinct()

            if status_filter == 'solved':
                queryset = queryset.filter(id__in=solved_ids)
            elif status_filter == 'unsolved':
                queryset = queryset.exclude(id__in=solved_ids)

        return queryset


class ProblemDetailView(generics.RetrieveAPIView):
    """
    GET /api/problems/<slug>/
    Get full problem details including test cases.
    """
    serializer_class = ProblemDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'
    queryset = Problem.objects.filter(is_active=True)


class TopicListView(generics.ListAPIView):
    """GET /api/problems/topics/ — All topics"""
    serializer_class = TopicSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Topic.objects.all()


class TagListView(generics.ListAPIView):
    """GET /api/problems/tags/ — All tags"""
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Tag.objects.all()


class RandomProblemView(APIView):
    """GET /api/problems/random/ — Get a random problem"""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        difficulty = request.query_params.get('difficulty')
        queryset = Problem.objects.filter(is_active=True)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty.upper())
        problem = queryset.order_by('?').first()
        if not problem:
            return Response({'error': 'No problems found.'}, status=404)
        return Response(ProblemDetailSerializer(problem).data)