from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, LoginView, LogoutView,
    MyProfileView, PublicProfileView,
    LeaderboardView, DailyProblemView, StreakView,
)

urlpatterns = [
    path('register/',       RegisterView.as_view()),
    path('login/',          LoginView.as_view()),
    path('logout/',         LogoutView.as_view()),
    path('token/refresh/',  TokenRefreshView.as_view()),
    path('profile/',        MyProfileView.as_view()),
    path('streak/',         StreakView.as_view()),
    path('leaderboard/',    LeaderboardView.as_view()),
    path('daily-problem/',  DailyProblemView.as_view()),
    path('<str:username>/', PublicProfileView.as_view()),
]