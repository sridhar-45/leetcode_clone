"""
backend/submissions/views.py
Copy this into backend/submissions/views.py
"""
import json
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from problems.models import Problem
from .models import Submission
from .serializers import SubmissionSerializer, SubmissionCreateSerializer
from .executor import CodeExecutor


class SubmitCodeView(APIView):
    """
    POST /api/submissions/submit/
    Receives user code, runs it, returns result.
    Requires authentication.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = SubmissionCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Get the problem
        try:
            problem = Problem.objects.get(
                slug=serializer.validated_data['problem_slug'],
                is_active=True
            )
        except Problem.DoesNotExist:
            return Response({'error': 'Problem not found.'}, status=404)

        # Create submission record (initially PENDING)
        submission = Submission.objects.create(
            user=request.user,
            problem=problem,
            code=serializer.validated_data['code'],
            language=serializer.validated_data['language'],
            status='RUNNING',
        )

        # Get ALL test cases (public + hidden)
        test_cases = list(problem.test_cases.values(
            'input_data', 'expected_output'
        ))

        if not test_cases:
            submission.status = 'RUNTIME_ERROR'
            submission.error_message = 'No test cases defined for this problem.'
            submission.save()
            return Response(SubmissionSerializer(submission).data)

        # Execute the code
        executor = CodeExecutor()
        result   = executor.execute(
            code=submission.code,
            language=submission.language,
            test_cases=test_cases
        )

        # Save results to submission
        submission.status             = result['status']
        submission.runtime            = result['runtime']
        submission.memory             = result['memory']
        submission.error_message      = result['error_message']
        submission.test_results       = json.dumps(result['test_results'])
        submission.test_cases_passed  = result['passed']
        submission.test_cases_total   = result['total']
        submission.save()

        # If accepted → update user stats + streak
        if submission.status == 'ACCEPTED':
            submission.post_accepted_actions()

        return Response(SubmissionSerializer(submission).data, status=200)


class RunCodeView(APIView):
    """
    POST /api/submissions/run/
    Run code against only the PUBLIC test cases (not all hidden ones).
    Used for the "Run Code" button (not Submit).
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        problem_slug = request.data.get('problem_slug')
        code         = request.data.get('code')
        language     = request.data.get('language', 'python')

        try:
            problem = Problem.objects.get(slug=problem_slug, is_active=True)
        except Problem.DoesNotExist:
            return Response({'error': 'Problem not found.'}, status=404)

        # Only public test cases for "Run"
        test_cases = list(problem.test_cases.filter(
            is_public=True
        ).values('input_data', 'expected_output'))

        executor = CodeExecutor()
        result   = executor.execute(code=code, language=language, test_cases=test_cases)

        return Response({
            'status':       result['status'],
            'runtime':      result['runtime'],
            'test_results': result['test_results'],
            'passed':       result['passed'],
            'total':        result['total'],
            'error_message': result['error_message'],
        })


class SubmissionListView(ListAPIView):
    """
    GET /api/submissions/
    List current user's submission history.
    """
    serializer_class   = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Submission.objects.filter(
            user=self.request.user
        ).select_related('problem')

    def list(self, request, *args, **kwargs):
        # Optional filter by problem
        problem_slug = request.query_params.get('problem')
        qs = self.get_queryset()
        if problem_slug:
            qs = qs.filter(problem__slug=problem_slug)
        serializer = self.get_serializer(qs[:50], many=True)  # limit 50
        return Response(serializer.data)


class SubmissionDetailView(APIView):
    """
    GET /api/submissions/<id>/
    Get details of a single submission.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            submission = Submission.objects.get(pk=pk, user=request.user)
        except Submission.DoesNotExist:
            return Response({'error': 'Not found.'}, status=404)
        return Response(SubmissionSerializer(submission).data)

