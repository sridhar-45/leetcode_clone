"""
backend/submissions/models.py
COMPLETE Submission model - Required by users and contests apps
"""

from django.db import models
from django.conf import settings
from problems.models import Problem


class Submission(models.Model):
    """
    Records every code submission made by users
    """

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('RUNNING', 'Running'),
        ('ACCEPTED', 'Accepted'),
        ('WRONG_ANSWER', 'Wrong Answer'),
        ('TIME_LIMIT_EXCEEDED', 'Time Limit Exceeded'),
        ('MEMORY_LIMIT_EXCEEDED', 'Memory Limit Exceeded'),
        ('RUNTIME_ERROR', 'Runtime Error'),
        ('COMPILE_ERROR', 'Compile Error'),
    ]

    LANGUAGE_CHOICES = [
        ('python', 'Python 3'),
        ('javascript', 'JavaScript'),
        ('java', 'Java'),
        ('cpp', 'C++'),
    ]

    # ===== RELATIONSHIPS =====
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='submissions'
    )

    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name='submissions'
    )

    # ===== SUBMISSION DETAILS =====
    code = models.TextField(help_text="User's submitted code")

    language = models.CharField(
        max_length=20,
        choices=LANGUAGE_CHOICES,
        default='python'
    )

    # ===== EXECUTION RESULTS =====
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    # Runtime in milliseconds
    runtime = models.IntegerField(
        null=True,
        blank=True,
        help_text="Execution time in ms"
    )

    # Memory in MB
    memory = models.FloatField(
        null=True,
        blank=True,
        help_text="Memory used in MB"
    )

    error_message = models.TextField(
        blank=True,
        help_text="Error output if failed"
    )

    # Test case results stored as JSON
    test_results = models.TextField(
        blank=True,
        help_text="JSON: [{input, expected, actual, passed, time}]"
    )

    # How many test cases passed
    test_cases_passed = models.IntegerField(default=0)
    test_cases_total = models.IntegerField(default=0)

    # ===== POINTS =====
    points_earned = models.IntegerField(
        default=0,
        help_text="Points earned for this submission"
    )

    is_first_accepted = models.BooleanField(
        default=False,
        help_text="True if this is the first accepted for this problem by user"
    )

    # ===== TIMESTAMPS =====
    created_at = models.DateTimeField(auto_now_add=True)
    executed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'submissions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'problem']),
            models.Index(fields=['status']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"{self.user.username} | {self.problem.title} | {self.status}"

    def is_accepted(self):
        return self.status == 'ACCEPTED'

    def post_accepted_actions(self):
        """
        Run after a submission is accepted.
        Updates user stats, streak, and points.
        """
        user = self.user
        problem = self.problem

        # Check if this is first time solving this problem
        previous_accepted = Submission.objects.filter(
            user=user,
            problem=problem,
            status='ACCEPTED',
        ).exclude(id=self.id).exists()

        if not previous_accepted:
            # First time solving - award points
            self.is_first_accepted = True
            self.points_earned = problem.points
            self.save(update_fields=['is_first_accepted', 'points_earned'])

            # Update user stats
            user.accepted_submissions += 1
            user.add_points(problem.points)
            user.save(update_fields=['accepted_submissions', 'total_points'])

            # Update detailed problem stats
            user.update_problem_stats()

            # Update daily streak
            user.update_streak()

        # Always increment total submissions count
        user.total_submissions += 1
        user.save(update_fields=['total_submissions'])

        # Update problem statistics
        problem.total_submissions += 1
        problem.accepted_submissions += 1
        problem.update_acceptance_rate()