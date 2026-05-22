import pytest
from django.urls import reverse
from rest_framework import status

from boards.models import TaskActivity

pytestmark = pytest.mark.django_db


def test_list_boards_as_owner(authenticated_client, board):
    url = reverse("boards:boards")

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["title"] == board.title


def test_list_boards_empty(authenticated_client):
    url = reverse("boards:boards")

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == []


def test_create_board(authenticated_client):
    url = reverse("boards:boards")
    data = {"title": "New Board", "description": "New Description"}

    response = authenticated_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == "New Board"
    assert response.data["description"] == "New Description"


def test_retrieve_board_as_owner(authenticated_client, board):
    url = reverse("boards:board-detail", kwargs={"pk": board.pk})

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == board.id


def test_retrieve_board_unauthorized(authenticated_client_another, board):
    url = reverse("boards:board-detail", kwargs={"pk": board.pk})

    response = authenticated_client_another.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_board_as_owner(authenticated_client, board):
    url = reverse("boards:board-detail", kwargs={"pk": board.pk})
    data = {"title": "Updated Title", "description": "Updated Description"}

    response = authenticated_client.put(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "Updated Title"


def test_update_board_unauthorized(authenticated_client_another, board):
    url = reverse("boards:board-detail", kwargs={"pk": board.pk})
    data = {"title": "Hacked Title"}

    response = authenticated_client_another.patch(url, data)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_board_as_owner(authenticated_client, board):
    url = reverse("boards:board-detail", kwargs={"pk": board.pk})

    response = authenticated_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_board_unauthorized(authenticated_client_another, board):
    url = reverse("boards:board-detail", kwargs={"pk": board.pk})

    response = authenticated_client_another.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_list_tasks(authenticated_client, task):
    url = reverse("boards:task-list")

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


def test_list_tasks_excludes_other_users_tasks(authenticated_client_another, task):
    url = reverse("boards:task-list")

    response = authenticated_client_another.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == []


def test_create_task(authenticated_client, board):
    url = reverse("boards:task-list")
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


def test_retrieve_task(authenticated_client, task):
    url = reverse("boards:task-detail", kwargs={"pk": task.pk})

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == task.id


def test_retrieve_task_unauthorized(authenticated_client_another, task):
    url = reverse("boards:task-detail", kwargs={"pk": task.pk})

    response = authenticated_client_another.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_task(authenticated_client, task):
    url = reverse("boards:task-detail", kwargs={"pk": task.pk})
    data = {"title": "Updated Task", "status": "IN_PROGRESS"}

    response = authenticated_client.patch(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "Updated Task"


def test_update_task_unauthorized(authenticated_client_another, task):
    url = reverse("boards:task-detail", kwargs={"pk": task.pk})
    data = {"title": "Hacked Task"}

    response = authenticated_client_another.patch(url, data)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_task(authenticated_client, task):
    url = reverse("boards:task-detail", kwargs={"pk": task.pk})

    response = authenticated_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_task_unauthorized(authenticated_client_another, task):
    url = reverse("boards:task-detail", kwargs={"pk": task.pk})

    response = authenticated_client_another.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_list_activities(authenticated_client, task, user):
    TaskActivity.objects.create(
        task=task,
        actor=user,
        action=TaskActivity.Action.CREATED,
    )
    url = reverse("boards:activities")

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) >= 1


def test_list_activities_excludes_other_users_activities(
    authenticated_client_another,
    task,
    user,
):
    TaskActivity.objects.create(
        task=task,
        actor=user,
        action=TaskActivity.Action.CREATED,
    )
    url = reverse("boards:activities")

    response = authenticated_client_another.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == []
