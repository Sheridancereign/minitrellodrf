from datetime import date, timedelta

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from boards.models import Board, Task

User = get_user_model()


@pytest.fixture
def db():
    pass


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )


@pytest.fixture
def another_user(db):
    return User.objects.create_user(
        username="anotheruser", email="another@example.com", password="anotherpass123"
    )


@pytest.fixture
def board(user):
    board = Board.objects.create(
        title="Test Board", description="Test Description", owner=user
    )
    board.members.add(user)
    return board


@pytest.fixture
def another_board(another_user):
    board = Board.objects.create(
        title="Another Board", description="Another Description", owner=another_user
    )
    board.members.add(another_user)
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


@pytest.fixture
def authenticated_client(api_client, user):
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return api_client


@pytest.fixture
def authenticated_client_another(api_client, another_user):
    refresh = RefreshToken.for_user(another_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return api_client
