
"""
═══════════════════════════════════════════════════════════════
FILE: backend/groups/urls.py
COPY ENTIRE CONTENT TO: backend/groups/urls.py
═══════════════════════════════════════════════════════════════
"""
from django.urls import path
from .views import (
    GroupListView, GroupDetailView, GroupCreateView,
    GroupJoinView, GroupLeaveView, GroupMembersView,
    MyGroupsView, GroupInviteView,
)

urlpatterns = [
    path('', GroupListView.as_view()),
    path('create/', GroupCreateView.as_view()),
    path('my/', MyGroupsView.as_view()),
    path('<slug:slug>/', GroupDetailView.as_view()),
    path('<slug:slug>/join/', GroupJoinView.as_view()),
    path('<slug:slug>/leave/', GroupLeaveView.as_view()),
    path('<slug:slug>/members/', GroupMembersView.as_view()),
    path('<slug:slug>/invite/', GroupInviteView.as_view()),
]


