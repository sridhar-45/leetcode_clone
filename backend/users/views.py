"""
backend/users/views.py
Copy this ENTIRE file into backend/users/views.py
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.utils import timezone
from .models import User, DailyProblem
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileUpdateSerializer,
    PublicUserSerializer,
    DailyProblemSerializer,
)


# ─────────────────────────────────────────
# HELPER: Generate tokens for a user
# ─────────────────────────────────────────
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access':  str(refresh.access_token),
    }


# ─────────────────────────────────────────
# 1. REGISTER  →  POST /api/users/register/
# ─────────────────────────────────────────
class RegisterView(APIView):
    """
    Create a new user account.
    Returns user data + JWT tokens.
    No authentication required.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user   = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response({
                'message': 'Account created successfully!',
                'user':    UserSerializer(user).data,
                'tokens':  tokens,
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ─────────────────────────────────────────
# 2. LOGIN  →  POST /api/users/login/
# ─────────────────────────────────────────
class LoginView(APIView):
    """
    Login with username + password.
    Returns user data + JWT tokens.
    No authentication required.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user   = serializer.validated_data['user']
            tokens = get_tokens_for_user(user)

            # Record last login
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])

            return Response({
                'message': 'Login successful!',
                'user':    UserSerializer(user).data,
                'tokens':  tokens,
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ─────────────────────────────────────────
# 3. LOGOUT  →  POST /api/users/logout/
# ─────────────────────────────────────────
class LogoutView(APIView):
    """
    Blacklist the refresh token (logout).
    Requires authentication.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'refresh': ['This field is required.']},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {'message': 'Logged out successfully.'},
                status=status.HTTP_200_OK
            )
        except TokenError:
            return Response(
                {'error': 'Invalid or expired refresh token.'},
                status=status.HTTP_400_BAD_REQUEST
            )


# ─────────────────────────────────────────
# 4. MY PROFILE  →  GET/PUT /api/users/profile/
# ─────────────────────────────────────────
class MyProfileView(APIView):
    """
    GET  → Return current user's full profile
    PUT  → Update profile fields (bio, location, etc.)
    Requires authentication.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileUpdateSerializer(
            request.user,
            data=request.data,
            partial=True       # Allow partial updates
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated!',
                'user': UserSerializer(request.user).data,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ─────────────────────────────────────────
# 5. PUBLIC PROFILE  →  GET /api/users/<username>/
# ─────────────────────────────────────────
class PublicProfileView(APIView):
    """
    View any user's public profile.
    No authentication required.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = PublicUserSerializer(user)
        return Response(serializer.data)


# ─────────────────────────────────────────
# 6. LEADERBOARD  →  GET /api/users/leaderboard/
# ─────────────────────────────────────────
class LeaderboardView(APIView):
    """
    Top users ranked by total points.
    No authentication required.
    Returns top 100 users.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        top_users = User.objects.filter(
            is_active=True
        ).order_by('-total_points', '-problems_solved')[:100]

        serializer = PublicUserSerializer(top_users, many=True)
        return Response({
            'count': top_users.count(),
            'users': serializer.data,
        })


# ─────────────────────────────────────────
# 7. DAILY PROBLEM  →  GET /api/users/daily-problem/
# ─────────────────────────────────────────
class DailyProblemView(APIView):
    """
    Get today's daily problem.
    Also shows if the current user already solved it.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        daily = DailyProblem.get_today_problem()

        if not daily:
            return Response(
                {'error': "No daily problem set for today."},
                status=status.HTTP_404_NOT_FOUND
            )

        completed = False
        if request.user.is_authenticated:
            completed = daily.completed_by.filter(id=request.user.id).exists()

        return Response({
            'daily_problem': DailyProblemSerializer(daily).data,
            'completed':     completed,
        })


# ─────────────────────────────────────────
# 8. STREAK INFO  →  GET /api/users/streak/
# ─────────────────────────────────────────
class StreakView(APIView):
    """
    Return current user's streak information.
    Requires authentication.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'current_streak':    user.current_streak,
            'longest_streak':    user.longest_streak,
            'last_activity':     user.last_activity_date,
            'is_on_streak':      user.is_on_streak,
            'total_points':      user.total_points,
            'global_ranking':    user.global_ranking,
        })
