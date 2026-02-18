"""
═══════════════════════════════════════════════════════════════
FILE: backend/contests/urls.py
COPY ENTIRE CONTENT TO: backend/contests/urls.py
═══════════════════════════════════════════════════════════════
"""
from django.urls import path
from .views import (
    ContestListView, ContestDetailView, ContestCreateView,
    ContestJoinView, ContestLeaderboardView,
    MyContestsView, MyCreatedContestsView,
)

urlpatterns = [
    path('', ContestListView.as_view()),
    path('create/', ContestCreateView.as_view()),
    path('my/', MyContestsView.as_view()),
    path('created/', MyCreatedContestsView.as_view()),
    path('<slug:slug>/', ContestDetailView.as_view()),
    path('<slug:slug>/join/', ContestJoinView.as_view()),
    path('<slug:slug>/leaderboard/', ContestLeaderboardView.as_view()),
]


