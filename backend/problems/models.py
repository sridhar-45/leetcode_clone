"""
backend/problems/models.py
COMPLETE Problem model - Required by users and contests apps
"""

from django.db import models
from django.utils.text import slugify


class Topic(models.Model):
    """Problem categories like Arrays, Trees, DP"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'topics'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """Specific tags like two-pointers, sliding-window"""
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'tags'
        ordering = ['name']

    def __str__(self):
        return self.name


class Problem(models.Model):
    """
    Main Problem model
    Stores all coding problems with their details
    """

    DIFFICULTY_CHOICES = [
        ('EASY', 'Easy'),
        ('MEDIUM', 'Medium'),
        ('HARD', 'Hard'),
    ]

    # Points awarded for solving (Easy=5, Medium=10, Hard=15)
    DIFFICULTY_POINTS = {
        'EASY': 5,
        'MEDIUM': 10,
        'HARD': 15,
    }

    # ===== BASIC INFO =====
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)

    description = models.TextField(
        help_text="Problem statement in Markdown format"
    )

    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='MEDIUM'
    )

    # ===== CONTENT =====
    constraints = models.TextField(
        blank=True,
        help_text="Problem constraints e.g. 1 <= n <= 10^5"
    )

    examples = models.TextField(
        blank=True,
        help_text="Example inputs and outputs"
    )

    hints = models.TextField(
        blank=True,
        help_text="Hints stored as JSON array"
    )

    # ===== CODE TEMPLATES =====
    template_python = models.TextField(
        default="class Solution:\n    def solve(self):\n        pass",
        help_text="Python starter code"
    )

    template_javascript = models.TextField(
        default="/**\n * @return {number}\n */\nvar solve = function() {\n    \n};",
        help_text="JavaScript starter code"
    )

    template_java = models.TextField(
        default="class Solution {\n    public void solve() {\n        \n    }\n}",
        help_text="Java starter code"
    )

    # ===== CATEGORIZATION =====
    topics = models.ManyToManyField(
        Topic,
        related_name='problems',
        blank=True
    )

    tags = models.ManyToManyField(
        Tag,
        related_name='problems',
        blank=True
    )

    # ===== STATISTICS =====
    total_submissions = models.IntegerField(default=0)
    accepted_submissions = models.IntegerField(default=0)
    acceptance_rate = models.FloatField(default=0.0)

    # ===== POINTS =====
    points = models.IntegerField(
        default=5,
        help_text="Points awarded for solving (auto-set by difficulty)"
    )

    # ===== FLAGS =====
    is_premium = models.BooleanField(default=False)
    is_active = models.BooleanField(
        default=True,
        help_text="Whether problem is visible to users"
    )

    # ===== DAILY PROBLEM =====
    is_daily = models.BooleanField(
        default=False,
        help_text="Currently selected as daily problem"
    )

    # ===== TIMESTAMPS =====
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'problems'
        ordering = ['id']
        verbose_name = 'Problem'
        verbose_name_plural = 'Problems'
        indexes = [
            models.Index(fields=['difficulty']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return f"{self.id}. {self.title} [{self.difficulty}]"

    def save(self, *args, **kwargs):
        # Auto-generate slug from title
        if not self.slug:
            self.slug = slugify(self.title)

        # Auto-set points based on difficulty
        self.points = self.DIFFICULTY_POINTS.get(self.difficulty, 5)

        super().save(*args, **kwargs)

    def update_acceptance_rate(self):
        """Recalculate acceptance rate after new submission"""
        if self.total_submissions > 0:
            self.acceptance_rate = round(
                (self.accepted_submissions / self.total_submissions) * 100, 1
            )
        self.save(update_fields=['acceptance_rate'])


class TestCase(models.Model):
    """
    Test cases for problems
    Used to validate user submissions
    """
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name='test_cases'
    )

    # Input and expected output stored as JSON strings
    input_data = models.TextField(
        help_text="Input as JSON e.g. [[2,7,11,15], 9]"
    )

    expected_output = models.TextField(
        help_text="Expected output as JSON e.g. [0,1]"
    )

    explanation = models.TextField(blank=True)

    is_public = models.BooleanField(
        default=True,
        help_text="Public cases shown to users, hidden cases used for final validation"
    )

    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'test_cases'
        ordering = ['order']

    def __str__(self):
        return f"TestCase {self.order} for {self.problem.title}"