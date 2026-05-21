import pytest

from boards.permissions import IsBoardOwner


@pytest.mark.django_db
class TestIsBoardOwnerPermission:
    def test_has_object_permission_as_owner(self, board, user):
        from rest_framework.test import APIRequestFactory

        factory = APIRequestFactory()
        request = factory.get("/")
        request.user = user

        permission = IsBoardOwner()
        assert permission.has_object_permission(request, None, board) is True

    def test_has_object_permission_not_owner(self, board, another_user):
        from rest_framework.test import APIRequestFactory

        factory = APIRequestFactory()
        request = factory.get("/")
        request.user = another_user

        permission = IsBoardOwner()
        assert permission.has_object_permission(request, None, board) is False
