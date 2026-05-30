"""
═══════════════════════════════════════════════════════════════
COMPLETE ENHANCED CONTEST SYSTEM
Individual Contests + Group Contests + All Features
═══════════════════════════════════════════════════════════════

LOCATION: backend/contests/models.py
REPLACE YOUR ENTIRE FILE WITH THIS
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify
import secrets
import string
import random
from datetime import timedelta

User = get_user_model()


# ═══════════════════════════════════════════════════════════════
# INDIVIDUAL CONTEST MODELS
# ═══════════════════════════════════════════════════════════════

class Contest(models.Model):
    """
    Main Contest Model - Supports both Individual and Group contests
    
    LOGIC:
    - If contest_type = 'INDIVIDUAL': Users join individually
    - If contest_type = 'GROUP': Groups join as teams
    
    PROBLEM ASSIGNMENT MODES:
    - 'SAME_FOR_ALL': All participants get same problems
    - 'UNIQUE_RANDOM': Each participant gets unique random problems
    - 'MANUAL': Creator manually selects problems
    """
    
    CONTEST_TYPE_CHOICES = [
        ('INDIVIDUAL', 'Individual Contest'),
        ('GROUP', 'Group/Team Contest'),
    ]
    
    PROBLEM_ASSIGNMENT_CHOICES = [
        ('SAME_FOR_ALL', 'Same problems for everyone'),
        ('UNIQUE_RANDOM', 'Unique random problems per participant'),
        ('MANUAL', 'Manually selected problems'),
    ]
    
    # Basic Info
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    
    # Contest Type
    contest_type = models.CharField(
        max_length=20, 
        choices=CONTEST_TYPE_CHOICES, 
        default='INDIVIDUAL'
    )
    
    # Creator
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='created_contests'
    )
    is_official = models.BooleanField(default=False)
    
    # Timing
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration_minutes = models.IntegerField(default=120)
    
    # Join Settings
    join_code = models.CharField(max_length=8, unique=True, blank=True)
    invite_link = models.CharField(max_length=100, unique=True, blank=True)
    is_public = models.BooleanField(default=True)
    
    # Participant Limits
    max_participants = models.IntegerField(default=1000)
    min_participants = models.IntegerField(default=1)
    
    # Problem Settings
    problem_assignment_mode = models.CharField(
        max_length=20,
        choices=PROBLEM_ASSIGNMENT_CHOICES,
        default='SAME_FOR_ALL'
    )
    problems_count = models.IntegerField(default=5)  # How many problems
    
    # Notifications
    send_notifications = models.BooleanField(default=True)
    notification_before_minutes = models.IntegerField(default=30)  # Notify 30 min before
    
    # Recurring Contest (like LeetCode Weekly)
    is_recurring = models.BooleanField(default=False)
    recurrence_pattern = models.CharField(
        max_length=50,
        blank=True,
        help_text="e.g., 'WEEKLY_SUNDAY', 'WEEKLY_SATURDAY', 'DAILY'"
    )
    
    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-start_time']
        indexes = [
            models.Index(fields=['contest_type', 'start_time']),
            models.Index(fields=['is_recurring', 'recurrence_pattern']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
            self.slug = f"{base_slug}-{unique_id}"
        
        if not self.join_code:
            self.join_code = self.generate_join_code()
        
        if not self.invite_link:
            self.invite_link = f"contest-{secrets.token_urlsafe(16)}"
        
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_join_code():
        """Generate unique 8-character join code"""
        return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    
    @property
    def status(self):
        """Get contest status"""
        now = timezone.now()
        if now < self.start_time:
            return 'UPCOMING'
        elif self.start_time <= now <= self.end_time:
            return 'LIVE'
        else:
            return 'ENDED'
    
    @property
    def total_participants(self):
        """Get total number of participants"""
        if self.contest_type == 'INDIVIDUAL':
            return self.individual_participants.count()
        else:
            return self.group_participants.count()
    
    @property
    def time_until_start(self):
        """Time remaining until contest starts"""
        if self.status == 'UPCOMING':
            delta = self.start_time - timezone.now()
            return delta.total_seconds()
        return 0
    
    @property
    def time_remaining(self):
        """Time remaining in contest"""
        if self.status == 'LIVE':
            delta = self.end_time - timezone.now()
            return delta.total_seconds()
        return 0
    
    def should_send_notification(self):
        """Check if notification should be sent"""
        if not self.send_notifications:
            return False
        
        now = timezone.now()
        notification_time = self.start_time - timedelta(minutes=self.notification_before_minutes)
        
        # Send notification if we're within the notification window
        return notification_time <= now < self.start_time
    
    def assign_problems_to_participant(self, participant):
        """
        Assign problems to a participant based on assignment mode
        
        LOGIC:
        1. SAME_FOR_ALL: Use problems from ContestProblem
        2. UNIQUE_RANDOM: Randomly select unique problems
        3. MANUAL: Use manually selected problems
        """
        from problems.models import Problem
        
        if self.problem_assignment_mode == 'SAME_FOR_ALL':
            # All participants get same problems (already in ContestProblem)
            return True
        
        elif self.problem_assignment_mode == 'UNIQUE_RANDOM':
            # Each participant gets unique random problems
            all_problems = list(Problem.objects.filter(is_active=True))
            
            if len(all_problems) < self.problems_count:
                raise ValueError(f"Not enough problems. Need at least {self.problems_count}")
            
            # Get problems already assigned to other participants
            assigned_problem_ids = ParticipantProblem.objects.filter(
                participant__contest=self
            ).values_list('problem_id', flat=True)
            
            # Get available problems
            available_problems = [p for p in all_problems if p.id not in assigned_problem_ids]
            
            # If not enough unique problems, allow overlap
            if len(available_problems) < self.problems_count:
                available_problems = all_problems
            
            # Randomly select problems
            selected_problems = random.sample(available_problems, self.problems_count)
            
            # Assign to participant
            for order, problem in enumerate(selected_problems):
                ParticipantProblem.objects.create(
                    participant=participant,
                    problem=problem,
                    order=order,
                    points=problem.points
                )
            
            return True
        
        elif self.problem_assignment_mode == 'MANUAL':
            # Use manually selected problems from ContestProblem
            return True
        
        return False
    
    def create_next_recurring_instance(self):
        """Create next instance of recurring contest"""
        if not self.is_recurring:
            return None
        
        # Calculate next start time based on pattern
        if self.recurrence_pattern == 'WEEKLY_SUNDAY':
            next_start = self.start_time + timedelta(days=7)
        elif self.recurrence_pattern == 'WEEKLY_SATURDAY':
            next_start = self.start_time + timedelta(days=7)
        elif self.recurrence_pattern == 'DAILY':
            next_start = self.start_time + timedelta(days=1)
        else:
            return None
        
        next_end = next_start + timedelta(minutes=self.duration_minutes)
        
        # Create new contest instance
        new_contest = Contest.objects.create(
            title=self.title,
            description=self.description,
            contest_type=self.contest_type,
            created_by=self.created_by,
            is_official=self.is_official,
            start_time=next_start,
            end_time=next_end,
            duration_minutes=self.duration_minutes,
            is_public=self.is_public,
            max_participants=self.max_participants,
            min_participants=self.min_participants,
            problem_assignment_mode=self.problem_assignment_mode,
            problems_count=self.problems_count,
            send_notifications=self.send_notifications,
            notification_before_minutes=self.notification_before_minutes,
            is_recurring=True,
            recurrence_pattern=self.recurrence_pattern
        )
        
        # Copy problems if SAME_FOR_ALL or MANUAL mode
        if self.problem_assignment_mode in ['SAME_FOR_ALL', 'MANUAL']:
            for cp in self.contest_problems.all():
                ContestProblem.objects.create(
                    contest=new_contest,
                    problem=cp.problem,
                    order=cp.order,
                    points=cp.points
                )
        
        return new_contest
    
    def __str__(self):
        return f"{self.title} ({self.get_contest_type_display()})"


class ContestProblem(models.Model):
    """
    Problems in a contest (for SAME_FOR_ALL and MANUAL modes)
    
    LOGIC:
    - Used when all participants get same problems
    - Creator manually selects these problems when creating contest
    """
    contest = models.ForeignKey(
        Contest, 
        on_delete=models.CASCADE, 
        related_name='contest_problems'
    )
    problem = models.ForeignKey('problems.Problem', on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    points = models.IntegerField(default=0)  # Custom points for this contest
    
    class Meta:
        unique_together = ['contest', 'problem']
        ordering = ['order']
    
    def __str__(self):
        return f"{self.problem.title} in {self.contest.title}"


class ContestParticipation(models.Model):
    """
    Individual participation in a contest
    
    LOGIC:
    - One record per user per contest
    - Tracks score, rank, problems solved
    - Automatically updated when user submits code
    """
    contest = models.ForeignKey(
        Contest, 
        on_delete=models.CASCADE, 
        related_name='individual_participants'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contest_participations')
    
    # Scoring
    total_score = models.IntegerField(default=0)
    problems_solved = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    time_penalty = models.IntegerField(default=0)  # Penalty in minutes
    
    # Timestamps
    joined_at = models.DateTimeField(auto_now_add=True)
    last_submission_at = models.DateTimeField(null=True, blank=True)
    
    # Notifications
    notification_sent = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['contest', 'user']
        ordering = ['-total_score', 'time_penalty']
        indexes = [
            models.Index(fields=['contest', '-total_score']),
        ]
    
    def calculate_score(self):
        """
        Calculate total score from submissions
        
        LOGIC:
        1. Get all user's accepted submissions for this contest
        2. Sum up points from unique problems
        3. Update total_score and problems_solved
        """
        from submissions.models import Submission
        
        # Get contest problems
        if self.contest.problem_assignment_mode == 'UNIQUE_RANDOM':
            # Use participant-specific problems
            problem_ids = self.assigned_problems.values_list('problem_id', flat=True)
        else:
            # Use common contest problems
            problem_ids = self.contest.contest_problems.values_list('problem_id', flat=True)
        
        # Get accepted submissions
        accepted_submissions = Submission.objects.filter(
            user=self.user,
            problem_id__in=problem_ids,
            status='ACCEPTED',
            created_at__gte=self.contest.start_time,
            created_at__lte=self.contest.end_time
        ).values('problem_id').annotate(
            first_accepted=models.Min('created_at')
        )
        
        total = 0
        solved = 0
        
        for sub in accepted_submissions:
            # Get points for this problem
            if self.contest.problem_assignment_mode == 'UNIQUE_RANDOM':
                try:
                    points = self.assigned_problems.get(problem_id=sub['problem_id']).points
                except:
                    points = 0
            else:
                try:
                    points = self.contest.contest_problems.get(problem_id=sub['problem_id']).points
                except:
                    points = 0
            
            total += points
            solved += 1
        
        self.total_score = total
        self.problems_solved = solved
        self.save()
        
        return total
    
    def __str__(self):
        return f"{self.user.username} in {self.contest.title}"


class ParticipantProblem(models.Model):
    """
    Problems assigned to a specific participant (UNIQUE_RANDOM mode only)
    
    LOGIC:
    - Only used when problem_assignment_mode = 'UNIQUE_RANDOM'
    - Each participant gets their own set of random problems
    - Tracks which problems are assigned to which participant
    """
    participant = models.ForeignKey(
        ContestParticipation, 
        on_delete=models.CASCADE, 
        related_name='assigned_problems'
    )
    problem = models.ForeignKey('problems.Problem', on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    
    # Tracking
    is_solved = models.BooleanField(default=False)
    solved_at = models.DateTimeField(null=True, blank=True)
    attempts = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['participant', 'problem']
        ordering = ['order']
    
    def __str__(self):
        return f"{self.problem.title} for {self.participant.user.username}"


class ContestSubmission(models.Model):
    """
    Link between submissions and contests
    
    LOGIC:
    - Created automatically when user submits during contest
    - Links regular Submission to Contest
    - Used for contest-specific statistics
    """
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    participant = models.ForeignKey(ContestParticipation, on_delete=models.CASCADE)
    submission = models.ForeignKey('submissions.Submission', on_delete=models.CASCADE)
    problem = models.ForeignKey('problems.Problem', on_delete=models.CASCADE)
    
    points_earned = models.IntegerField(default=0)
    time_from_start = models.IntegerField(default=0)  # Minutes from contest start
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['contest', 'participant']),
        ]
    
    def __str__(self):
        return f"Submission by {self.participant.user.username} in {self.contest.title}"


class ContestNotification(models.Model):
    """
    Notifications sent to contest participants
    
    LOGIC:
    - Created when contest is about to start
    - Sent to all registered participants
    - Tracks delivery status
    """
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    notification_type = models.CharField(max_length=50, default='CONTEST_STARTING')
    message = models.TextField()
    
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"Notification to {self.user.username} for {self.contest.title}"


"""
═══════════════════════════════════════════════════════════════
HOW THE LOGIC CONNECTS - COMPLETE FLOW EXPLANATION
═══════════════════════════════════════════════════════════════

SCENARIO 1: INDIVIDUAL CONTEST - SAME PROBLEMS FOR ALL
──────────────────────────────────────────────────────

Step 1: Creator Creates Contest
    Contest.objects.create(
        title="Weekly Challenge",
        contest_type='INDIVIDUAL',
        problem_assignment_mode='SAME_FOR_ALL',
        problems_count=5,
        start_time=...,
        end_time=...
    )
    
    Creator manually selects 5 problems:
    ContestProblem.create(contest=contest, problem=prob1, points=10)
    ContestProblem.create(contest=contest, problem=prob2, points=15)
    ... (5 problems total)

Step 2: Users Join
    User A joins → ContestParticipation created
    User B joins → ContestParticipation created
    ... All users get SAME 5 problems

Step 3: During Contest
    User A submits solution to Problem 1:
        - Submission created
        - ContestSubmission created (links to contest)
        - If ACCEPTED: points added to User A's score
        - ContestParticipation.calculate_score() called
        - Leaderboard updated

Step 4: After Contest
    System calculates final ranks
    Winners announced


SCENARIO 2: INDIVIDUAL CONTEST - UNIQUE RANDOM PROBLEMS
────────────────────────────────────────────────────────

Step 1: Creator Creates Contest
    Contest.objects.create(
        title="Random Challenge",
        contest_type='INDIVIDUAL',
        problem_assignment_mode='UNIQUE_RANDOM',
        problems_count=7,  # Each user gets 7 random problems
        ...
    )
    
    NO manual problem selection needed!

Step 2: User A Joins
    - ContestParticipation created for User A
    - System randomly selects 7 problems from database
    - Creates ParticipantProblem for each:
        ParticipantProblem(participant=user_a, problem=random_prob_1)
        ParticipantProblem(participant=user_a, problem=random_prob_5)
        ... (7 unique random problems)

Step 3: User B Joins
    - ContestParticipation created for User B
    - System randomly selects 7 DIFFERENT problems
    - Creates ParticipantProblem for each:
        ParticipantProblem(participant=user_b, problem=random_prob_3)
        ParticipantProblem(participant=user_b, problem=random_prob_9)
        ... (7 unique random problems, different from User A)

Step 4: During Contest
    User A can only see/solve their 7 assigned problems
    User B can only see/solve their 7 assigned problems
    Scores calculated based on their specific problems


SCENARIO 3: RECURRING CONTEST (Like LeetCode Weekly)
─────────────────────────────────────────────────────

Step 1: Create First Instance
    Contest.objects.create(
        title="Weekly Contest #1",
        is_recurring=True,
        recurrence_pattern='WEEKLY_SUNDAY',
        start_time=datetime(2026, 3, 23, 10, 0),  # Sunday 10 AM
        ...
    )

Step 2: After Contest Ends
    Automated task (Celery) runs:
        contest.create_next_recurring_instance()
    
    Creates:
        "Weekly Contest #2"
        start_time=datetime(2026, 3, 30, 10, 0)  # Next Sunday
    
    Copies all settings and problems from #1

Step 3: Continues Forever
    Each week, new instance created automatically
    Users can join each week's contest


SCENARIO 4: NOTIFICATIONS
──────────────────────────

Step 1: Contest Starting in 30 Minutes
    System checks: contest.should_send_notification()
    Returns True if current_time >= (start_time - 30 minutes)

Step 2: Send Notifications
    For each participant:
        ContestNotification.objects.create(
            contest=contest,
            user=participant.user,
            message="Your contest starts in 30 minutes!"
        )
    
    Email/Push notification sent

Step 3: User Receives Alert
    Opens app/email
    Sees notification
    Clicks to join contest


SCENARIO 5: INVITE FRIENDS
───────────────────────────

Step 1: Creator Gets Invite Link
    contest.invite_link = "contest-xyz123abc456"
    
    Full link: https://yoursite.com/contests/join/contest-xyz123abc456

Step 2: Share Link
    Creator sends link to friends via:
    - Email
    - WhatsApp
    - Social media

Step 3: Friend Clicks Link
    - Redirected to contest page
    - Can join directly if public
    - Asked for join_code if private
    - Auto-registered as participant


DATABASE RELATIONSHIPS
──────────────────────

Contest (1) ←→ (Many) ContestProblem
    "A contest has many problems"

Contest (1) ←→ (Many) ContestParticipation
    "A contest has many participants"

ContestParticipation (1) ←→ (Many) ParticipantProblem
    "Each participant has their own set of problems (UNIQUE_RANDOM mode)"

ContestParticipation (1) ←→ (Many) ContestSubmission
    "Each participant makes many submissions"

Submission (1) ←→ (1) ContestSubmission
    "Links regular submissions to contests"
"""