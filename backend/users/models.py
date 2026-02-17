"""
USER MODEL - Complete Implementation
Includes: Authentication, Profile, Statistics, Daily Streak
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    """
    Custom User Model
    
    INHERITED FIELDS from AbstractUser:
    - username: unique username
    - email: email address  
    - password: hashed password
    - first_name, last_name
    - is_active, is_staff, is_superuser
    - date_joined, last_login
    
    CUSTOM FIELDS:
    - Profile information
    - Problem-solving statistics
    - Daily streak tracking
    - Points and ranking
    """
    
    # ========== PROFILE INFORMATION ==========
    bio = models.TextField(
        max_length=500,
        blank=True,
        help_text="User biography"
    )
    
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        help_text="Profile picture"
    )
    
    location = models.CharField(
        max_length=100,
        blank=True
    )
    
    website = models.URLField(
        max_length=200,
        blank=True
    )
    
    github_username = models.CharField(
        max_length=100,
        blank=True
    )
    
    # ========== PROBLEM STATISTICS ==========
    problems_solved = models.IntegerField(
        default=0,
        help_text="Total unique problems solved"
    )
    
    easy_solved = models.IntegerField(default=0)
    medium_solved = models.IntegerField(default=0)
    hard_solved = models.IntegerField(default=0)
    
    total_submissions = models.IntegerField(
        default=0,
        help_text="Total code submissions"
    )
    
    accepted_submissions = models.IntegerField(
        default=0,
        help_text="Successfully accepted submissions"
    )
    
    # ========== POINTS & RANKING ==========
    total_points = models.IntegerField(
        default=0,
        help_text="Total points earned (Easy:5, Medium:10, Hard:15)"
    )
    
    global_ranking = models.IntegerField(
        default=0,
        help_text="Global rank based on points"
    )
    
    # ========== DAILY STREAK TRACKING ==========
    current_streak = models.IntegerField(
        default=0,
        help_text="Current consecutive days of solving problems"
    )
    
    longest_streak = models.IntegerField(
        default=0,
        help_text="Longest streak ever achieved"
    )
    
    last_activity_date = models.DateField(
        null=True,
        blank=True,
        help_text="Last day user solved a problem"
    )
    
    # ========== CONTEST STATS ==========
    contests_participated = models.IntegerField(
        default=0,
        help_text="Number of contests participated in"
    )
    
    contests_won = models.IntegerField(
        default=0,
        help_text="Number of contests won (rank 1)"
    )
    
    # ========== TIMESTAMPS ==========
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        ordering = ['-total_points', '-problems_solved']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['total_points', '-problems_solved']),
            models.Index(fields=['global_ranking']),
        ]
    
    def __str__(self):
        return self.username
    
    # ========== DAILY STREAK METHODS ==========
    
    def update_streak(self):
        """
        Update user's daily streak
        Called when user solves a problem
        
        Logic:
        - If today: increment streak
        - If yesterday: continue streak
        - If gap > 1 day: reset to 1
        """
        today = timezone.now().date()
        
        # First problem ever
        if not self.last_activity_date:
            self.current_streak = 1
            self.longest_streak = 1
            self.last_activity_date = today
            self.save()
            return
        
        # Already solved today
        if self.last_activity_date == today:
            return
        
        yesterday = today - timedelta(days=1)
        
        # Solved yesterday - continue streak
        if self.last_activity_date == yesterday:
            self.current_streak += 1
            if self.current_streak > self.longest_streak:
                self.longest_streak = self.current_streak
        
        # Gap in solving - reset streak
        else:
            self.current_streak = 1
        
        self.last_activity_date = today
        self.save()
    
    def check_streak_broken(self):
        """
        Check if streak is broken (missed yesterday)
        Run this daily via cron job
        """
        if not self.last_activity_date:
            return
        
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        
        # Missed yesterday - reset streak
        if self.last_activity_date < yesterday:
            self.current_streak = 0
            self.save()
    
    # ========== STATISTICS METHODS ==========
    
    def update_problem_stats(self):
        """
        Recalculate all problem statistics
        Called after accepting a submission
        """
        from submissions.models import Submission
        
        # Count unique problems solved by difficulty
        solved_problems = Submission.objects.filter(
            user=self,
            status='ACCEPTED'
        ).values('problem__id', 'problem__difficulty').distinct()
        
        self.easy_solved = solved_problems.filter(
            problem__difficulty='EASY'
        ).count()
        
        self.medium_solved = solved_problems.filter(
            problem__difficulty='MEDIUM'
        ).count()
        
        self.hard_solved = solved_problems.filter(
            problem__difficulty='HARD'
        ).count()
        
        self.problems_solved = (
            self.easy_solved + 
            self.medium_solved + 
            self.hard_solved
        )
        
        # Calculate total points
        self.total_points = (
            (self.easy_solved * 5) +
            (self.medium_solved * 10) +
            (self.hard_solved * 15)
        )
        
        self.save()
    
    def add_points(self, points):
        """
        Add points when solving a problem
        
        Args:
            points: Points to add (5/10/15)
        """
        self.total_points += points
        self.save()
    
    def update_global_ranking(self):
        """
        Update user's global rank
        Run periodically or after point changes
        """
        # Count users with more points
        higher_ranked = User.objects.filter(
            total_points__gt=self.total_points
        ).count()
        
        self.global_ranking = higher_ranked + 1
        self.save()
    
    # ========== PROPERTY METHODS ==========
    
    @property
    def acceptance_rate(self):
        """Calculate submission acceptance rate"""
        if self.total_submissions == 0:
            return 0.0
        return (self.accepted_submissions / self.total_submissions) * 100
    
    @property
    def is_on_streak(self):
        """Check if user is currently on a streak"""
        if not self.last_activity_date:
            return False
        
        today = timezone.now().date()
        return self.last_activity_date >= today - timedelta(days=1)
    
    @property
    def profile_completion(self):
        """Calculate profile completion percentage"""
        fields = [
            self.first_name,
            self.last_name,
            self.bio,
            self.location,
            self.website,
            self.github_username,
            self.avatar,
        ]
        filled = sum(1 for f in fields if f)
        return (filled / len(fields)) * 100


# ========== DAILY PROBLEM MODEL ==========

class DailyProblem(models.Model):
    """
    Daily problem selection
    One problem per day for all users
    """
    date = models.DateField(
        unique=True,
        help_text="Date for this daily problem"
    )
    
    problem = models.ForeignKey(
        'problems.Problem',
        on_delete=models.CASCADE,
        related_name='daily_selections'
    )
    
    completed_by = models.ManyToManyField(
        User,
        through='DailyProblemCompletion',
        related_name='completed_daily_problems'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'daily_problems'
        ordering = ['-date']
        verbose_name = 'Daily Problem'
        verbose_name_plural = 'Daily Problems'
    
    def __str__(self):
        return f"Daily Problem: {self.date} - {self.problem.title}"
    
    @classmethod
    def get_today_problem(cls):
        """Get today's daily problem"""
        today = timezone.now().date()
        try:
            return cls.objects.get(date=today)
        except cls.DoesNotExist:
            return None


class DailyProblemCompletion(models.Model):
    """
    Track which users completed today's problem
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    
    daily_problem = models.ForeignKey(
        DailyProblem,
        on_delete=models.CASCADE
    )
    
    completed_at = models.DateTimeField(auto_now_add=True)
    
    submission = models.ForeignKey(
        'submissions.Submission',
        on_delete=models.SET_NULL,
        null=True
    )
    
    class Meta:
        db_table = 'daily_problem_completions'
        unique_together = ['user', 'daily_problem']
        verbose_name = 'Daily Problem Completion'
        verbose_name_plural = 'Daily Problem Completions'
    
    def __str__(self):
        return f"{self.user.username} completed {self.daily_problem.date}"