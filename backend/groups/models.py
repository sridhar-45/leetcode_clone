"""
GROUP MODELS - Group Battle System
Features:
- Create groups (min 2 members)
- Join with code
- Group contests
- Group leaderboard
- Group vs Group competitions
"""

from django.db import models
from django.conf import settings
from django.utils import timezone
import secrets
import string


def generate_group_code():
    """Generate unique 6-character group code"""
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))


class Group(models.Model):
    """
    Group/Team Model
    Users can create groups to compete together
    """
    
    # ========== BASIC INFO ==========
    name = models.CharField(
        max_length=100,
        help_text="Group name"
    )
    
    description = models.TextField(
        max_length=500,
        blank=True,
        help_text="Group description"
    )
    
    slug = models.SlugField(
        max_length=120,
        unique=True
    )
    
    avatar = models.ImageField(
        upload_to='group_avatars/',
        blank=True,
        null=True,
        help_text="Group avatar/logo"
    )
    
    # ========== CREATOR & ADMIN ==========
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_groups',
        help_text="Group creator/admin"
    )
    
    # ========== JOIN CODE ==========
    join_code = models.CharField(
        max_length=6,
        unique=True,
        default=generate_group_code,
        help_text="Code to join group"
    )
    
    is_public = models.BooleanField(
        default=True,
        help_text="If False, requires join_code"
    )
    
    # ========== MEMBER LIMITS ==========
    max_members = models.IntegerField(
        default=50,
        help_text="Maximum group members"
    )
    
    current_members = models.IntegerField(
        default=1,
        help_text="Current member count"
    )
    
    # ========== GROUP STATISTICS ==========
    total_points = models.IntegerField(
        default=0,
        help_text="Combined points of all members"
    )
    
    total_problems_solved = models.IntegerField(
        default=0,
        help_text="Total unique problems solved by group"
    )
    
    contests_participated = models.IntegerField(
        default=0,
        help_text="Number of contests participated"
    )
    
    contests_won = models.IntegerField(
        default=0,
        help_text="Number of contests won"
    )
    
    global_rank = models.IntegerField(
        default=0,
        help_text="Rank among all groups"
    )
    
    # ========== STATUS ==========
    is_active = models.BooleanField(
        default=True,
        help_text="Whether group is currently active"
    )
    
    # ========== TIMESTAMPS ==========
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'groups'
        ordering = ['-total_points']
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
        indexes = [
            models.Index(fields=['join_code']),
            models.Index(fields=['-total_points']),
        ]
    
    def __str__(self):
        return self.name
    
    # ========== MEMBER MANAGEMENT ==========
    
    def can_join(self, user):
        """Check if user can join this group"""
        # Already a member
        if self.members.filter(user=user).exists():
            return False, "Already a member"
        
        # Group full
        if self.current_members >= self.max_members:
            return False, "Group is full"
        
        # Group inactive
        if not self.is_active:
            return False, "Group is inactive"
        
        return True, "Can join"
    
    def add_member(self, user, role='MEMBER'):
        """
        Add user to group
        Returns: (success, message)
        """
        can_join, message = self.can_join(user)
        if not can_join:
            return False, message
        
        # Create membership
        membership = GroupMember.objects.create(
            group=self,
            user=user,
            role=role
        )
        
        # Update member count
        self.current_members += 1
        self.save()
        
        # Recalculate group stats
        self.update_statistics()
        
        return True, "Successfully joined group"
    
    def remove_member(self, user):
        """Remove user from group"""
        try:
            membership = self.members.get(user=user)
            membership.delete()
            
            self.current_members -= 1
            self.save()
            
            # Recalculate stats
            self.update_statistics()
            
            return True, "Member removed"
        except GroupMember.DoesNotExist:
            return False, "User is not a member"
    
    # ========== STATISTICS METHODS ==========
    
    def update_statistics(self):
        """
        Recalculate group statistics
        Sum of all members' contributions
        """
        members = self.members.select_related('user').all()
        
        # Sum total points
        self.total_points = sum(m.points_contributed for m in members)
        
        # Count unique problems solved by group
        from submissions.models import Submission
        solved_problems = Submission.objects.filter(
            user__in=[m.user for m in members],
            status='ACCEPTED'
        ).values('problem__id').distinct().count()
        
        self.total_problems_solved = solved_problems
        
        self.save()
    
    def update_global_rank(self):
        """Update group's global ranking"""
        higher_ranked = Group.objects.filter(
            total_points__gt=self.total_points,
            is_active=True
        ).count()
        
        self.global_rank = higher_ranked + 1
        self.save()
    
    # ========== PROPERTY METHODS ==========
    
    @property
    def average_points_per_member(self):
        """Calculate average points per member"""
        if self.current_members == 0:
            return 0
        return self.total_points // self.current_members
    
    @property
    def is_full(self):
        """Check if group is at max capacity"""
        return self.current_members >= self.max_members


class GroupMember(models.Model):
    """
    Group membership
    Tracks individual member contributions
    """
    
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('MEMBER', 'Member'),
    ]
    
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='members'
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='group_memberships'
    )
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='MEMBER'
    )
    
    # ========== CONTRIBUTIONS ==========
    points_contributed = models.IntegerField(
        default=0,
        help_text="Points earned while in group"
    )
    
    problems_solved = models.IntegerField(
        default=0,
        help_text="Problems solved while in group"
    )
    
    # ========== TIMESTAMPS ==========
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'group_members'
        unique_together = ['group', 'user']
        ordering = ['-points_contributed']
        verbose_name = 'Group Member'
        verbose_name_plural = 'Group Members'
    
    def __str__(self):
        return f"{self.user.username} in {self.group.name}"
    
    def is_admin(self):
        """Check if member is admin"""
        return self.role == 'ADMIN' or self.user == self.group.created_by
    
    def add_contribution(self, points):
        """Add points contribution"""
        self.points_contributed += points
        self.problems_solved += 1
        self.save()
        
        # Update group stats
        self.group.update_statistics()


class GroupContest(models.Model):
    """
    Contest between groups
    Each group competes as a team
    """
    contest = models.ForeignKey(
        'contests.Contest',
        on_delete=models.CASCADE,
        related_name='group_contests'
    )
    
    participating_groups = models.ManyToManyField(
        Group,
        through='GroupContestParticipation',
        related_name='contests'
    )
    
    # ========== SETTINGS ==========
    min_groups = models.IntegerField(
        default=2,
        help_text="Minimum groups required"
    )
    
    max_groups = models.IntegerField(
        default=10,
        help_text="Maximum groups allowed"
    )
    
    # ========== STATUS ==========
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'group_contests'
        verbose_name = 'Group Contest'
        verbose_name_plural = 'Group Contests'
    
    def __str__(self):
        return f"Group Battle: {self.contest.title}"
    
    def get_leaderboard(self):
        """Get group rankings for this contest"""
        return self.participations.select_related('group').order_by(
            '-total_score',
            'time_penalty'
        )


class GroupContestParticipation(models.Model):
    """
    Group participation in a contest
    Aggregates scores of all group members
    """
    group_contest = models.ForeignKey(
        GroupContest,
        on_delete=models.CASCADE,
        related_name='participations'
    )
    
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='contest_participations'
    )
    
    # ========== GROUP SCORE ==========
    total_score = models.IntegerField(
        default=0,
        help_text="Combined score of all members"
    )
    
    problems_solved = models.IntegerField(
        default=0,
        help_text="Unique problems solved by group"
    )
    
    rank = models.IntegerField(
        default=0,
        help_text="Rank in this contest"
    )
    
    time_penalty = models.IntegerField(
        default=0,
        help_text="Average time penalty of members"
    )
    
    # ========== TIMESTAMPS ==========
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'group_contest_participations'
        unique_together = ['group_contest', 'group']
        ordering = ['-total_score']
    
    def __str__(self):
        return f"{self.group.name} in {self.group_contest.contest.title}"
    
    def update_score(self):
        """
        Recalculate group score
        Sum of all member scores in this contest
        """
        from contests.models import ContestParticipation
        
        contest = self.group_contest.contest
        group_members = self.group.members.values_list('user', flat=True)
        
        # Get all member participations
        member_participations = ContestParticipation.objects.filter(
            contest=contest,
            user__in=group_members
        )
        
        # Sum scores
        self.total_score = sum(p.total_score for p in member_participations)
        self.problems_solved = sum(p.problems_solved for p in member_participations)
        self.time_penalty = sum(p.time_penalty for p in member_participations)
        
        if member_participations.count() > 0:
            self.time_penalty //= member_participations.count()
        
        self.save()


class GroupInvitation(models.Model):
    """
    Group invitation sent to users
    """
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='invitations'
    )
    
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_invitations'
    )
    
    invited_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_invitations'
    )
    
    message = models.TextField(
        max_length=500,
        blank=True
    )
    
    # ========== STATUS ==========
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('DECLINED', 'Declined'),
    ]
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    
    # ========== TIMESTAMPS ==========
    sent_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'group_invitations'
        unique_together = ['group', 'invited_user']
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"Invitation to {self.invited_user.username} for {self.group.name}"
    
    def accept(self):
        """Accept invitation and join group"""
        self.status = 'ACCEPTED'
        self.responded_at = timezone.now()
        self.save()
        
        # Add user to group
        return self.group.add_member(self.invited_user)
    
    def decline(self):
        """Decline invitation"""
        self.status = 'DECLINED'
        self.responded_at = timezone.now()
        self.save()