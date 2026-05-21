import pytest

from boards.models import TaskActivity
from boards.serializers import BoardSerializer, TaskActivitySerializer, TaskSerializer


@pytest.mark.django_db
class TestBoardSerializer:
    def test_serialize_board(self, board):
        serializer = BoardSerializer(board)
        data = serializer.data
        assert data["id"] == board.id
        assert data["title"] == board.title
        assert data["description"] == board.description
        assert data["owner"] == board.owner.username
        assert "created_at" in data

    def test_board_fields(self):
        serializer = BoardSerializer()
        expected_fields = {"id", "title", "description", "owner", "created_at"}
        assert set(serializer.fields.keys()) == expected_fields


@pytest.mark.django_db
class TestTaskSerializer:
    def test_serialize_task(self, task):
        serializer = TaskSerializer(task)
        data = serializer.data
        assert data["id"] == task.id
        assert data["title"] == task.title
        assert data["description"] == task.description
        assert data["status"] == task.status
        assert data["priority"] == task.priority
        assert data["created_by"] == task.created_by.username
        assert "created_at" in data

    def test_task_fields(self):
        serializer = TaskSerializer()
        expected_fields = {
            "id",
            "title",
            "description",
            "status",
            "priority",
            "due_date",
            "board",
            "assignee",
            "created_at",
            "created_by",
        }
        assert set(serializer.fields.keys()) == expected_fields


@pytest.mark.django_db
class TestTaskActivitySerializer:
    def test_serialize_activity(self, task, user):
        activity = TaskActivity.objects.create(
            task=task,
            actor=user,
            action=TaskActivity.Action.CREATED,
            field="status",
            old_value="TODO",
            new_value="IN_PROGRESS",
        )
        serializer = TaskActivitySerializer(activity)
        data = serializer.data
        assert data["id"] == activity.id
        assert data["action"] == activity.action
        assert data["field"] == activity.field
        assert data["old_value"] == activity.old_value
        assert data["new_value"] == activity.new_value
        assert data["actor"] == activity.actor.username
        assert "created_at" in data

    def test_activity_fields(self):
        serializer = TaskActivitySerializer()
        expected_fields = {
            "id",
            "action",
            "field",
            "old_value",
            "new_value",
            "actor",
            "created_at",
        }
        assert set(serializer.fields.keys()) == expected_fields
