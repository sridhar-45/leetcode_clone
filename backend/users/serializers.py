"""
backend/users/serializers.py
Copy this ENTIRE file into backend/users/serializers.py
"""

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import User, DailyProblem, DailyProblemCompletion


# ─────────────────────────────────────────
# 1. USER SERIALIZER  (Read profile data)
# ─────────────────────────────────────────
class UserSerializer(serializers.ModelSerializer):
    """
    Used to READ user data.
    Returned after login/register and for profile page.
    """
    acceptance_rate = serializers.ReadOnlyField()
    is_on_streak    = serializers.ReadOnlyField()

    class Meta:
        model  = User
        fields = [
            'id', 'username', 'email',
            'first_name', 'last_name',
            'bio', 'avatar', 'location',
            'website', 'github_username',
            # stats
            'problems_solved',
            'easy_solved', 'medium_solved', 'hard_solved',
            'total_submissions', 'accepted_submissions',
            'acceptance_rate',
            # points & rank
            'total_points', 'global_ranking',
            # streak
            'current_streak', 'longest_streak',
            'last_activity_date', 'is_on_streak',
            # contest
            'contests_participated', 'contests_won',
            # meta
            'date_joined', 'updated_at',
        ]
        read_only_fields = [
            'id',
            'problems_solved', 'easy_solved', 'medium_solved', 'hard_solved',
            'total_submissions', 'accepted_submissions',
            'total_points', 'global_ranking',
            'current_streak', 'longest_streak',
            'contests_participated', 'contests_won',
            'date_joined', 'updated_at',
        ]


# ─────────────────────────────────────────
# 2. REGISTRATION SERIALIZER
# ─────────────────────────────────────────
class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Used to CREATE a new user account.
    Validates that passwords match.
    """
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        label="Confirm Password"
    )

    class Meta:
        model  = User
        fields = ['username', 'email', 'password', 'password2',
                  'first_name', 'last_name']
        extra_kwargs = {
            'email':      {'required': True, 'allow_blank': False},
            'password':   {'write_only': True, 'trim_whitespace': False},
            'first_name': {'required': False},
            'last_name':  {'required': False},
        }

    def validate_email(self, value):
        """Make sure email is unique"""
        value = value.strip().lower()
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate(self, attrs):
        """Make sure both passwords match"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        candidate_user = User(
            username=attrs.get('username', ''),
            email=attrs.get('email', ''),
            first_name=attrs.get('first_name', ''),
            last_name=attrs.get('last_name', ''),
        )
        try:
            validate_password(attrs['password'], user=candidate_user)
        except DjangoValidationError as exc:
            raise serializers.ValidationError({'password': exc.messages})
        return attrs

    def create(self, validated_data):
        """Create user with hashed password"""
        validated_data.pop('password2')
        user = User.objects.create_user(
            username   = validated_data['username'],
            email      = validated_data['email'],
            password   = validated_data['password'],
            first_name = validated_data.get('first_name', ''),
            last_name  = validated_data.get('last_name', ''),
        )
        return user


# ─────────────────────────────────────────
# 3. LOGIN SERIALIZER
# ─────────────────────────────────────────
class UserLoginSerializer(serializers.Serializer):
    """
    Validates login credentials.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            username=attrs['username'],
            password=attrs['password']
        )
        if not user:
            raise serializers.ValidationError("Invalid username or password.")
        if not user.is_active:
            raise serializers.ValidationError("This account has been disabled.")
        attrs['user'] = user
        return attrs


# ─────────────────────────────────────────
# 4. PROFILE UPDATE SERIALIZER
# ─────────────────────────────────────────
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Used to UPDATE profile info (bio, location, etc.)
    Does NOT allow changing password here.
    """
    class Meta:
        model  = User
        fields = [
            'first_name', 'last_name',
            'bio', 'avatar', 'location',
            'website', 'github_username',
        ]


# ─────────────────────────────────────────
# 5. PUBLIC USER SERIALIZER (Leaderboard / Other profiles)
# ─────────────────────────────────────────
class PublicUserSerializer(serializers.ModelSerializer):
    """
    Safe public view — hides email and private info.
    Used on leaderboard and public profile pages.
    """
    acceptance_rate = serializers.ReadOnlyField()

    class Meta:
        model  = User
        fields = [
            'id', 'username',
            'first_name', 'last_name',
            'avatar', 'location',
            'problems_solved',
            'easy_solved', 'medium_solved', 'hard_solved',
            'total_points', 'global_ranking',
            'current_streak', 'longest_streak',
            'acceptance_rate',
            'date_joined',
        ]


# ─────────────────────────────────────────
# 6. DAILY PROBLEM SERIALIZER
# ─────────────────────────────────────────
class DailyProblemSerializer(serializers.ModelSerializer):
    problem_title      = serializers.CharField(source='problem.title', read_only=True)
    problem_slug       = serializers.CharField(source='problem.slug', read_only=True)
    problem_difficulty = serializers.CharField(source='problem.difficulty', read_only=True)
    problem_points     = serializers.IntegerField(source='problem.points', read_only=True)

    class Meta:
        model  = DailyProblem
        fields = [
            'id', 'date',
            'problem_title', 'problem_slug',
            'problem_difficulty', 'problem_points',
        ]
