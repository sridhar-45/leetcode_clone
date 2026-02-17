"""
CONTEST MODELS - User-Created Contests
Features:
- Official LeetCode contests
- User-created contests
- Join with unique code
- Real-time leaderboard
- Time-based scoring
"""

from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import secrets
import string


def generate_join_code():
    """Generate unique 8-character join code"""
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))


class Contest(models.Model):
    """
    Contest Model
    
    Types:
    1. Official contests (created by admin)
    2. User-created contests (created by any user)
    """
    
    CONTEST_STATUS = [
        ('UPCOMING', 'Upcoming'),
        ('LIVE', 'Live'),
        ('FINISHED', 'Finished'),
    ]
    
    # ========== BASIC INFO ==========
    title = models.CharField(
        max_length=200,
        help_text="Contest title"
    )
    
    description = models.TextField(
        help_text="Contest description and rules"
    )
    
    slug = models.SlugField(
        max_length=250,
        unique=True
    )
    
    # ========== CREATOR INFO ==========
    is_official = models.BooleanField(
        default=False,
        help_text="True for LeetCode official contests"
    )
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_contests',
        help_text="User who created this contest"
    )
    
    # ========== JOIN CODE (FOR USER CONTESTS) ==========
    join_code = models.CharField(
        max_length=8,
        unique=True,
        default=generate_join_code,
        help_text="Unique code to join contest"
    )
    
    is_public = models.BooleanField(
        default=True,
        help_text="If False, needs join_code to participate"
    )
    
    # ========== TIME SETTINGS ==========
    start_time = models.DateTimeField(
        help_text="Contest start time"
    )
    
    end_time = models.DateTimeField(
        help_text="Contest end time"
    )
    
    duration_minutes = models.IntegerField(
        help_text="Contest duration in minutes"
    )
    
    # ========== PARTICIPANT LIMITS ==========
    max_participants = models.IntegerField(
        default=1000,
        help_text="Maximum number of participants (0 = unlimited)"
    )
    
    min_participants = models.IntegerField(
        default=2,
        help_text="Minimum participants required to start"
    )
    
    # ========== STATISTICS ==========
    total_participants = models.IntegerField(
        default=0,
        help_text="Number of registered participants"
    )
    
    # ========== TIMESTAMPS ==========
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'contests'
        ordering = ['-start_time']
        verbose_name = 'Contest'
        verbose_name_plural = 'Contests'
        indexes = [
            models.Index(fields=['start_time', 'end_time']),
            models.Index(fields=['is_official']),
            models.Index(fields=['join_code']),
        ]
    
    def __str__(self):
        return self.title
    
    # ========== STATUS METHODS ==========
    
    @property
    def status(self):
        """Get current contest status"""
        now = timezone.now()
        if now < self.start_time:
            return 'UPCOMING'
        elif now > self.end_time:
            return 'FINISHED'
        else:
            return 'LIVE'
    
    @property
    def is_live(self):
        """Check if contest is currently running"""
        now = timezone.now()
        return self.start_time <= now <= self.end_time
    
    @property
    def is_finished(self):
        """Check if contest has ended"""
        return timezone.now() > self.end_time
    
    @property
    def time_until_start(self):
        """Get time remaining until start"""
        if self.is_live or self.is_finished:
            return None
        delta = self.start_time - timezone.now()
        return delta
    
    @property
    def time_remaining(self):
        """Get time remaining in contest"""
        if not self.is_live:
            return None
        delta = self.end_time - timezone.now()
        return delta
    
    # ========== PARTICIPATION METHODS ==========
    
    def can_join(self, user):
        """Check if user can join this contest"""
        # Already participating
        if self.participants.filter(user=user).exists():
            return False, "Already registered"
        
        # Contest finished
        if self.is_finished:
            return False, "Contest has ended"
        
        # Max participants reached
        if self.max_participants > 0 and self.total_participants >= self.max_participants:
            return False, "Contest is full"
        
        return True, "Can join"
    
    def join_contest(self, user):
        """
        Join user to contest
        Returns: (success, message)
        """
        can_join, message = self.can_join(user)
        if not can_join:
            return False, message
        
        # Create participation
        participation = ContestParticipation.objects.create(
            contest=self,
            user=user
        )
        
        # Update total participants
        self.total_participants += 1
        self.save()
        
        return True, "Successfully joined contest"
    
    def get_leaderboard(self):
        """
        Get contest leaderboard
        Sorted by: total_score DESC, time_penalty ASC
        """
        return self.participants.select_related('user').order_by(
            '-total_score',
            'time_penalty'
        )
    
    def update_participant_ranks(self):
        """Update ranks for all participants"""
        leaderboard = self.get_leaderboard()
        for rank, participation in enumerate(leaderboard, start=1):
            participation.rank = rank
            participation.save(update_fields=['rank'])


class ContestProblem(models.Model):
    """
    Problems in a contest
    Many-to-many relationship with ordering
    """
    contest = models.ForeignKey(
        Contest,
        on_delete=models.CASCADE,
        related_name='contest_problems'
    )
    
    problem = models.ForeignKey(
        'problems.Problem',
        on_delete=models.CASCADE,
        related_name='in_contests'
    )
    
    order = models.IntegerField(
        default=0,
        help_text="Display order in contest"
    )
    
    points = models.IntegerField(
        help_text="Points for solving this problem in contest"
    )
    
    class Meta:
        db_table = 'contest_problems'
        ordering = ['order']
        unique_together = ['contest', 'problem']
    
    def __str__(self):
        return f"{self.contest.title} - {self.problem.title}"


class ContestParticipation(models.Model):
    """
    User participation in a contest
    Tracks score, rank, and performance
    """
    contest = models.ForeignKey(
        Contest,
        on_delete=models.CASCADE,
        related_name='participants'
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='contest_participations'
    )
    
    # ========== SCORE & RANKING ==========
    total_score = models.IntegerField(
        default=0,
        help_text="Total points earned in contest"
    )
    
    problems_solved = models.IntegerField(
        default=0,
        help_text="Number of problems solved"
    )
    
    rank = models.IntegerField(
        default=0,
        help_text="Current rank in contest"
    )
    
    # ========== TIME PENALTY ==========
    time_penalty = models.IntegerField(
        default=0,
        help_text="Total time in seconds (for ranking tiebreaker)"
    )
    
    # ========== TIMESTAMPS ==========
    joined_at = models.DateTimeField(auto_now_add=True)
    last_submission_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'contest_participations'
        ordering = ['-total_score', 'time_penalty']
        unique_together = ['contest', 'user']
        verbose_name = 'Contest Participation'
        verbose_name_plural = 'Contest Participations'
        indexes = [
            models.Index(fields=['contest', '-total_score']),
        ]
    
    def __str__(self):
        return f"{self.user.username} in {self.contest.title}"
    
    def add_solved_problem(self, problem, submission_time):
        """
        Update score when user solves a problem
        
        Args:
            problem: ContestProblem instance
            submission_time: When problem was solved
        """
        # Calculate time penalty (seconds since contest start)
        time_taken = (submission_time - self.contest.start_time).total_seconds()
        
        self.total_score += problem.points
        self.problems_solved += 1
        self.time_penalty += int(time_taken)
        self.last_submission_at = submission_time
        self.save()
        
        # Update contest-wide ranks
        self.contest.update_participant_ranks()


class ContestSubmission(models.Model):
    """
    Submission made during a contest
    Links to regular submission
    """
    participation = models.ForeignKey(
        ContestParticipation,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    
    contest_problem = models.ForeignKey(
        ContestProblem,
        on_delete=models.CASCADE
    )
    
    submission = models.ForeignKey(
        'submissions.Submission',
        on_delete=models.CASCADE,
        related_name='contest_submission'
    )
    
    points_earned = models.IntegerField(
        default=0,
        help_text="Points earned for this submission"
    )
    
    submission_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'contest_submissions'
        ordering = ['-submission_time']
    
    def __str__(self):
        return f"{self.participation.user.username} - {self.contest_problem.problem.title}"