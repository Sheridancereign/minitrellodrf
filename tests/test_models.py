import pytest

from boards.models import Board, Task, TaskActivity


@pytest.mark.django_db
class TestBoardModel:
    def test_board_creation(self, user):
        board = Board.objects.create(
            title="Test Board", description="Test Description", owner=user
        )
        assert board.title == "Test Board"
        assert board.description == "Test Description"
        assert board.owner == user
        assert str(board) == "Test Board"

    def test_board_members(self, board, user, another_user):
        board.members.add(another_user)
        assert user in board.members.all()
        assert another_user in board.members.all()

    def test_board_created_at_auto(self, user):
        board = Board.objects.create(title="Test Board", owner=user)
        assert board.created_at is not None


@pytest.mark.django_db
class TestTaskModel:
    def test_task_creation(self, task):
        assert task.title == "Test Task"
        assert task.description == "Test Task Description"
        assert task.status == Task.Status.TODO
        assert task.priority == Task.Priority.MEDIUM
        assert str(task) == "Test Task"

    def test_task_status_choices(self):
        assert Task.Status.TODO == "TODO"
        assert Task.Status.IN_PROGRESS == "IN_PROGRESS"
        assert Task.Status.DONE == "DONE"

    def test_task_priority_choices(self):
        assert Task.Priority.LOW == "LOW"
        assert Task.Priority.MEDIUM == "MEDIUM"
        assert Task.Priority.HIGH == "HIGH"

    def test_task_due_date_optional(self, board, user):
        task = Task.objects.create(
            title="Task without due date", board=board, created_by=user
        )
        assert task.due_date is None

    def test_task_assignee_optional(self, board, user):
        task = Task.objects.create(
            title="Task without assignee", board=board, created_by=user
        )
        assert task.assignee is None


@pytest.mark.django_db
class TestTaskActivityModel:
    def test_activity_creation(self, task, user):
        activity = TaskActivity.objects.create(
            task=task,
            actor=user,
            action=TaskActivity.Action.CREATED,
            field="status",
            old_value="TODO",
            new_value="IN_PROGRESS",
        )
        assert activity.task == task
        assert activity.actor == user
        assert activity.action == TaskActivity.Action.CREATED

    def test_activity_action_choices(self):
        assert TaskActivity.Action.CREATED == "CREATED"
        assert TaskActivity.Action.STATUS_CHANGED == "STATUS_CHANGED"
        assert TaskActivity.Action.ASSIGNEE_CHANGED == "ASSIGNEE_CHANGED"
        assert TaskActivity.Action.UPDATED == "UPDATED"

    def test_activity_str_representation(self, task):
        activity = TaskActivity.objects.create(
            task=task, actor=task.created_by, action=TaskActivity.Action.CREATED
        )
        assert "CREATED" in str(activity)
        assert task.title in str(activity)
