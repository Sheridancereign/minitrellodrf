from datetime import date, timedelta

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from boards.models import Board, BoardMembership, Task
from users.management.commands.setup_roles import ROLE_PERMISSIONS
from users.permissions import PermissionGroups

User = get_user_model()


def assign_group(user, group_name):
    group = Group.objects.get(name=group_name)
    user.groups.clear()
    user.groups.add(group)
    return user


@pytest.fixture(autouse=True)
def permission_groups(db):
    for group_name, codenames in ROLE_PERMISSIONS.items():
        group, _ = Group.objects.get_or_create(name=group_name)
        permissions = Permission.objects.filter(
            content_type__app_label="boards",
            codename__in=codenames,
        )
        group.permissions.set(permissions)


@pytest.fixture
def grant_role():
    return assign_group


@pytest.fixture
def user(db):
    user = User.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    return assign_group(user, PermissionGroups.MEMBER)


@pytest.fixture
def another_user(db):
    user = User.objects.create_user(
        username="anotheruser", email="another@example.com", password="anotherpass123"
    )
    return assign_group(user, PermissionGroups.MEMBER)


@pytest.fixture
def board_member_user(db):
    user = User.objects.create_user(
        username="boardmember",
        email="boardmember@example.com",
        password="memberpass123",
    )
    return assign_group(user, PermissionGroups.MEMBER)


@pytest.fixture
def superuser(db):
    return User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="adminpass123",
    )


@pytest.fixture
def board(user):
    board = Board.objects.create(
        title="Test Board", description="Test Description", owner=user
    )
    BoardMembership.objects.create(
        board=board,
        user=user,
    )
    return board


@pytest.fixture
def another_board(another_user):
    board = Board.objects.create(
        title="Another Board", description="Another Description", owner=another_user
    )
    BoardMembership.objects.create(
        board=board,
        user=another_user,
    )
    return board


@pytest.fixture
def task(board, user):
    return Task.objects.create(
        title="Test Task",
        description="Test Task Description",
        status=Task.Status.TODO,
        priority=Task.Priority.MEDIUM,
        board=board,
        created_by=user,
        assignee=user,
    )


@pytest.fixture
def future_date():
    return date.today() + timedelta(days=7)


@pytest.fixture
def past_date():
    return date.today() - timedelta(days=7)


@pytest.fixture
def api_client():
    return APIClient()


def get_authenticated_client(user):
    api_client = APIClient()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return api_client


@pytest.fixture
def authenticated_client(user):
    return get_authenticated_client(user)


@pytest.fixture
def authenticated_client_another(another_user):
    return get_authenticated_client(another_user)


@pytest.fixture
def authenticated_client_superuser(superuser):
    return get_authenticated_client(superuser)
