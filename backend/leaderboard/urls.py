"""
═══════════════════════════════════════════════════════════════
FILE: backend/leaderboard/urls.py
COPY ENTIRE CONTENT TO: backend/leaderboard/urls.py
═══════════════════════════════════════════════════════════════
"""
from django.urls import path
from .views import GlobalLeaderboardView, GroupLeaderboardView

urlpatterns = [
    path('global/', GlobalLeaderboardView.as_view()),
    path('groups/', GroupLeaderboardView.as_view()),
]