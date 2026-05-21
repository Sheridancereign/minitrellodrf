import pytest

from boards.dto.task_dto import CreateTaskDTO, UpdateTaskDTO
from boards.exceptions import TaskDomainException
from boards.models import Task, TaskActivity
from boards.services.activity_service import ActivityService
from boards.services.task_service import TaskService


@pytest.mark.django_db
class TestTaskService:
    def test_create_task_success(self, board, user):
        dto = CreateTaskDTO(
            title="New Task",
            description="Description",
            status=Task.Status.TODO,
            priority=Task.Priority.HIGH,
            board=board,
            assignee=user,
        )
        task = TaskService.create_task(dto=dto, user=user)
        assert task.title == "New Task"
        assert task.board == board
        assert task.created_by == user

    def test_create_task_not_owner_raises_exception(self, board, another_user):
        dto = CreateTaskDTO(title="New Task", board=board, assignee=another_user)
        with pytest.raises(TaskDomainException) as exc_info:
            TaskService.create_task(dto=dto, user=another_user)
        assert "not the owner" in str(exc_info.value)

    def test_create_task_done_without_assignee_raises_exception(self, board, user):
        dto = CreateTaskDTO(
            title="New Task", board=board, status=Task.Status.DONE, assignee=None
        )
        with pytest.raises(TaskDomainException) as exc_info:
            TaskService.create_task(dto=dto, user=user)
        assert "cannot be DONE without assignee" in str(exc_info.value)

    def test_create_task_past_due_date_raises_exception(self, board, user, past_date):
        dto = CreateTaskDTO(title="New Task", board=board, due_date=past_date)
        with pytest.raises(TaskDomainException) as exc_info:
            TaskService.create_task(dto=dto, user=user)
        assert "Due date cannot be in the past" in str(exc_info.value)

    def test_create_task_assignee_not_member_raises_exception(
        self, board, user, another_user
    ):
        dto = CreateTaskDTO(title="New Task", board=board, assignee=another_user)
        with pytest.raises(TaskDomainException) as exc_info:
            TaskService.create_task(dto=dto, user=user)
        assert "Assignee must be board member" in str(exc_info.value)

    def test_update_task_success(self, task, user):
        dto = UpdateTaskDTO(title="Updated Title", status=Task.Status.IN_PROGRESS)
        updated_task = TaskService.update_task(task=task, dto=dto)
        assert updated_task.title == "Updated Title"
        assert updated_task.status == Task.Status.IN_PROGRESS

    def test_update_done_task_raises_exception(self, task):
        task.status = Task.Status.DONE
        task.save()
        dto = UpdateTaskDTO(title="Should fail")
        with pytest.raises(TaskDomainException) as exc_info:
            TaskService.update_task(task=task, dto=dto)
        assert "Done tasks cannot be modified" in str(exc_info.value)

    def test_update_task_past_due_date_raises_exception(self, task, past_date):
        dto = UpdateTaskDTO(due_date=past_date)
        with pytest.raises(TaskDomainException) as exc_info:
            TaskService.update_task(task=task, dto=dto)
        assert "Due date cannot be in the past" in str(exc_info.value)

    def test_update_task_to_done_without_assignee_raises_exception(self, task):
        task.assignee = None
        task.save()
        dto = UpdateTaskDTO(status=Task.Status.DONE)
        with pytest.raises(TaskDomainException) as exc_info:
            TaskService.update_task(task=task, dto=dto)
        assert "DONE task requires assignee" in str(exc_info.value)


@pytest.mark.django_db
class TestActivityService:
    def test_log_task_created(self, task, user):
        ActivityService.log_task_created(task=task, actor=user)
        assert TaskActivity.objects.filter(task=task).count() == 1
        activity = TaskActivity.objects.first()
        assert activity.action == TaskActivity.Action.CREATED
        assert activity.actor == user

    def test_log_field_change(self, task, user):
        ActivityService.log_field_change(
            task=task,
            actor=user,
            field="status",
            old_value="TODO",
            new_value="IN_PROGRESS",
            action=TaskActivity.Action.STATUS_CHANGED,
        )
        assert TaskActivity.objects.filter(task=task).count() == 1
        activity = TaskActivity.objects.first()
        assert activity.action == TaskActivity.Action.STATUS_CHANGED
        assert activity.field == "status"
        assert activity.old_value == "TODO"
        assert activity.new_value == "IN_PROGRESS"
