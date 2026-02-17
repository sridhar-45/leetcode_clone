"""
backend/leaderboard/models.py
"""

from django.db import models
from django.conf import settings


class UserRanking(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ranking_entry'
    )
    rank = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    problems_solved = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_rankings'
        ordering = ['rank']

    def __str__(self):
        return f"Rank {self.rank}: {self.user.username}"