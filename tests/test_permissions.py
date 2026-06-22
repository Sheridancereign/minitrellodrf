import pytest
from rest_framework.test import APIRequestFactory

from boards.permissions import IsBoardOwner
from boards.services import permission_service
from users.permissions import PermissionGroups

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


def test_can_assign_task_allows_manager(user, grant_role):
    grant_role(user, PermissionGroups.MANAGER)

    assert permission_service.can_assign_task(user=user) is True


def test_can_assign_task_allows_superuser(superuser):
    assert permission_service.can_assign_task(user=superuser) is True


def test_can_assign_task_denies_regular_member(another_user):
    assert permission_service.can_assign_task(user=another_user) is False


def test_can_manage_board_members_allows_manager(user, grant_role):
    grant_role(user, PermissionGroups.MANAGER)

    assert permission_service.can_manage_board_members(user=user) is True


def test_can_manage_board_members_denies_regular_member(another_user):
    assert permission_service.can_manage_board_members(user=another_user) is False
