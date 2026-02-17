from django.urls import path
from .views import (
    ProblemListView, ProblemDetailView,
    TopicListView, TagListView, RandomProblemView,
)

urlpatterns = [
    path('',           ProblemListView.as_view()),
    path('topics/',    TopicListView.as_view()),
    path('tags/',      TagListView.as_view()),
    path('random/',    RandomProblemView.as_view()),
    path('<slug:slug>/', ProblemDetailView.as_view()),
]