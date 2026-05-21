import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestBoardViews:
    def test_list_boards_as_owner(self, authenticated_client, board):
        url = reverse("boards")
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["title"] == board.title

    def test_list_boards_empty(self, authenticated_client):
        url = reverse("boards")
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_create_board(self, authenticated_client):
        url = reverse("boards")
        data = {"title": "New Board", "description": "New Description"}
        response = authenticated_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == "New Board"
        assert response.data["description"] == "New Description"

    def test_retrieve_board_as_owner(self, authenticated_client, board):
        url = reverse("board-detail", kwargs={"pk": board.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == board.id

    def test_retrieve_board_unauthorized(self, authenticated_client_another, board):
        url = reverse("board-detail", kwargs={"pk": board.pk})
        response = authenticated_client_another.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_board_as_owner(self, authenticated_client, board):
        url = reverse("board-detail", kwargs={"pk": board.pk})
        data = {"title": "Updated Title", "description": "Updated Description"}
        response = authenticated_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Updated Title"

    def test_update_board_unauthorized(self, authenticated_client_another, board):
        url = reverse("board-detail", kwargs={"pk": board.pk})
        data = {"title": "Hacked Title"}
        response = authenticated_client_another.put(url, data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_board_as_owner(self, authenticated_client, board):
        url = reverse("board-detail", kwargs={"pk": board.pk})
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_board_unauthorized(self, authenticated_client_another, board):
        url = reverse("board-detail", kwargs={"pk": board.pk})
        response = authenticated_client_another.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestTaskViews:
    def test_list_tasks(self, authenticated_client, task):
        url = reverse("task-list")
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_create_task(self, authenticated_client, board, user):
        url = reverse("task-list")
        data = {
            "title": "New Task",
            "description": "New Task Description",
            "status": "TODO",
            "priority": "HIGH",
            "board": board.id,
        }
        response = authenticated_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == "New Task"

    def test_retrieve_task(self, authenticated_client, task):
        url = reverse("task-detail", kwargs={"pk": task.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == task.id

    def test_update_task(self, authenticated_client, task):
        url = reverse("task-detail", kwargs={"pk": task.pk})
        data = {"title": "Updated Task", "status": "IN_PROGRESS"}
        response = authenticated_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Updated Task"

    def test_delete_task(self, authenticated_client, task):
        url = reverse("task-detail", kwargs={"pk": task.pk})
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestTaskActivityViews:
    def test_list_activities(self, authenticated_client, task, user):
        from boards.models import TaskActivity

        TaskActivity.objects.create(
            task=task, actor=user, action=TaskActivity.Action.CREATED
        )
        url = reverse("boards:activities")
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
