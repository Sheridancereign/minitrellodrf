import pytest

from boards.dto.task_dto import CreateTaskDTO, UpdateTaskDTO
from boards.models import BoardMembership, Task, TaskActivity
from boards.services import activity_service, task_service
from users.permissions import PermissionGroups

pytestmark = pytest.mark.django_db


def test_create_task_success(board, user):
    dto = CreateTaskDTO(
        title="New Task",
        description="Description",
        status=Task.Status.TODO,
        priority=Task.Priority.HIGH,
        board=board,
        assignee=user,
    )

    task = task_service.create_task(dto=dto, user=user)

    assert task.title == "New Task"
    assert task.board == board
    assert task.created_by == user


def test_create_task_logs_activity(board, user):
    dto = CreateTaskDTO(title="New Task", board=board, assignee=user)

    task = task_service.create_task(dto=dto, user=user)

    activity = TaskActivity.objects.get(task=task)
    assert activity.action == TaskActivity.Action.CREATED
    assert activity.actor == user


def test_create_task_not_owner_raises_exception(board, another_user):
    dto = CreateTaskDTO(title="New Task", board=board, assignee=another_user)

    with pytest.raises(ValueError) as exc_info:
        task_service.create_task(dto=dto, user=another_user)

    assert "not the owner" in str(exc_info.value)


def test_create_task_done_without_assignee_raises_exception(board, user):
    dto = CreateTaskDTO(
        title="New Task",
        board=board,
        status=Task.Status.DONE,
        assignee=None,
    )

    with pytest.raises(ValueError) as exc_info:
        task_service.create_task(dto=dto, user=user)

    assert "cannot be DONE without assignee" in str(exc_info.value)


def test_create_task_past_due_date_raises_exception(board, user, past_date):
    dto = CreateTaskDTO(title="New Task", board=board, due_date=past_date)

    with pytest.raises(ValueError) as exc_info:
        task_service.create_task(dto=dto, user=user)

    assert "Due date cannot be in the past" in str(exc_info.value)


def test_create_task_assignee_not_member_raises_exception(board, user, another_user):
    dto = CreateTaskDTO(title="New Task", board=board, assignee=another_user)

    with pytest.raises(ValueError) as exc_info:
        task_service.create_task(dto=dto, user=user)

    assert "Assignee must be board member" in str(exc_info.value)


def test_update_task_success(task, user):
    dto = UpdateTaskDTO(title="Updated Title", status=Task.Status.IN_PROGRESS)

    updated_task = task_service.update_task(task=task, dto=dto, actor=user)

    assert updated_task.title == "Updated Title"
    assert updated_task.status == Task.Status.IN_PROGRESS


def test_update_task_logs_status_change(task, user):
    dto = UpdateTaskDTO(status=Task.Status.IN_PROGRESS)

    task_service.update_task(task=task, dto=dto, actor=user)

    activity = TaskActivity.objects.get(
        task=task,
        action=TaskActivity.Action.STATUS_CHANGED,
    )
    assert activity.actor == user
    assert activity.field == "status"
    assert activity.old_value == Task.Status.TODO
    assert activity.new_value == Task.Status.IN_PROGRESS


def test_update_done_task_raises_exception(task, user):
    task.status = Task.Status.DONE
    task.save()
    dto = UpdateTaskDTO(title="Should fail")

    with pytest.raises(ValueError) as exc_info:
        task_service.update_task(task=task, dto=dto, actor=user)

    assert "Done tasks cannot be modified" in str(exc_info.value)


def test_update_task_past_due_date_raises_exception(task, user, past_date):
    dto = UpdateTaskDTO(due_date=past_date)

    with pytest.raises(ValueError) as exc_info:
        task_service.update_task(task=task, dto=dto, actor=user)

    assert "Due date cannot be in the past" in str(exc_info.value)


def test_update_task_to_done_without_assignee_raises_exception(task, user):
    task.assignee = None
    task.save()
    dto = UpdateTaskDTO(status=Task.Status.DONE)

    with pytest.raises(ValueError) as exc_info:
        task_service.update_task(task=task, dto=dto, actor=user)

    assert "DONE task requires assignee" in str(exc_info.value)


def test_assign_task_success(task, user, another_user, grant_role):
    grant_role(user, PermissionGroups.MANAGER)
    BoardMembership.objects.create(
        board=task.board,
        user=another_user,
    )

    updated_task = task_service.assign_task(
        task=task,
        assignee=another_user,
        actor=user,
    )

    assert updated_task.assignee == another_user


def test_assign_task_logs_assignee_change(task, user, another_user, grant_role):
    grant_role(user, PermissionGroups.MANAGER)
    BoardMembership.objects.create(
        board=task.board,
        user=another_user,
    )

    task_service.assign_task(task=task, assignee=another_user, actor=user)

    activity = TaskActivity.objects.get(
        task=task,
        action=TaskActivity.Action.ASSIGNEE_CHANGED,
    )
    assert activity.actor == user
    assert activity.field == "assignee"
    assert activity.old_value == str(user)
    assert activity.new_value == str(another_user)


def test_assign_task_denies_regular_member_actor(task, user, another_user):
    BoardMembership.objects.create(
        board=task.board,
        user=another_user,
    )

    with pytest.raises(ValueError) as exc_info:
        task_service.assign_task(task=task, assignee=user, actor=another_user)

    assert "permission to assign tasks" in str(exc_info.value)


def test_assign_task_denies_non_member_assignee(task, user, another_user, grant_role):
    grant_role(user, PermissionGroups.MANAGER)

    with pytest.raises(ValueError) as exc_info:
        task_service.assign_task(task=task, assignee=another_user, actor=user)

    assert "Assignee must be board member" in str(exc_info.value)


def test_log_task_created(task, user):
    activity_service.log_task_created(task=task, actor=user)

    activity = TaskActivity.objects.get(task=task)
    assert activity.action == TaskActivity.Action.CREATED
    assert activity.actor == user


def test_log_field_change(task, user):
    activity_service.log_field_change(
        task=task,
        actor=user,
        field="status",
        old_value="TODO",
        new_value="IN_PROGRESS",
        action=TaskActivity.Action.STATUS_CHANGED,
    )

    activity = TaskActivity.objects.get(task=task)
    assert activity.action == TaskActivity.Action.STATUS_CHANGED
    assert activity.field == "status"
    assert activity.old_value == "TODO"
    assert activity.new_value == "IN_PROGRESS"
