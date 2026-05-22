import pytest
from rest_framework.test import APIRequestFactory

from boards.models import BoardMembership
from boards.permissions import IsBoardOwner
from boards.services import permission_service

pytestmark = pytest.mark.django_db


def test_is_board_owner_allows_owner(board, user):
    request = APIRequestFactory().get("/")
    request.user = user

    permission = IsBoardOwner()

    assert permission.has_object_permission(request, None, board) is True


def test_is_board_owner_denies_non_owner(board, another_user):
    request = APIRequestFactory().get("/")
    request.user = another_user

    permission = IsBoardOwner()

    assert permission.has_object_permission(request, None, board) is False


def test_can_assign_task_allows_owner(board, user):
    assert permission_service.can_assign_task(user=user, board=board) is True


def test_can_assign_task_allows_manager(board, another_user):
    BoardMembership.objects.create(
        board=board,
        user=another_user,
        role=BoardMembership.Role.MANAGER,
    )

    assert permission_service.can_assign_task(user=another_user, board=board) is True


def test_can_assign_task_denies_regular_member(board, another_user):
    BoardMembership.objects.create(
        board=board,
        user=another_user,
        role=BoardMembership.Role.MEMBER,
    )

    assert permission_service.can_assign_task(user=another_user, board=board) is False


def test_can_assign_task_denies_non_member(board, another_user):
    assert permission_service.can_assign_task(user=another_user, board=board) is False
