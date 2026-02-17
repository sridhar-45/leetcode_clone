"""
backend/submissions/urls.py
Copy this into backend/submissions/urls.py
"""
from django.urls import path
from .views import (
    SubmitCodeView, RunCodeView,
    SubmissionListView, SubmissionDetailView,
)

urlpatterns = [
    path('submit/', SubmitCodeView.as_view()),
    path('run/',    RunCodeView.as_view()),
    path('',        SubmissionListView.as_view()),
    path('<int:pk>/', SubmissionDetailView.as_view()),
]