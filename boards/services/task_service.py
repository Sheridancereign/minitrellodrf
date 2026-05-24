from datetime import date

from boards.dto.task_dto import CreateTaskDTO, UpdateTaskDTO
from boards.exceptions import TaskDomainException
from boards.models import Task, TaskActivity
from boards.services import activity_service, permission_service


def create_task(*, dto: CreateTaskDTO, user):
    board = dto.board

    if board.owner != user:
        raise TaskDomainException("You are not the owner of this board")

    if dto.status == Task.Status.DONE and dto.assignee is None:
        raise TaskDomainException("Task cannot be DONE without assignee")

    if dto.due_date and dto.due_date < date.today():
        raise TaskDomainException("Due date cannot be in the past")

    if dto.assignee and dto.assignee not in board.members.all():
        raise TaskDomainException("Assignee must be board member")

    task = Task.objects.create(
        title=dto.title,
        description=dto.description,
        status=dto.status,
        priority=dto.priority,
        due_date=dto.due_date,
        board=dto.board,
        assignee=dto.assignee,
        created_by=user,
    )

    activity_service.log_task_created(
        task=task,
        actor=user,
    )

    return task


def update_task(*, task: Task, dto: UpdateTaskDTO, actor=None):
    actor = actor or task.created_by
    assignee_was_set = "assignee" in dto.model_fields_set

    if task.status == Task.Status.DONE:
        raise TaskDomainException("Done tasks cannot be modified")

    if dto.due_date and dto.due_date < date.today():
        raise TaskDomainException("Due date cannot be in the past")

    next_status = dto.status or task.status

    next_assignee = dto.assignee if assignee_was_set else task.assignee

    if next_status == Task.Status.DONE and next_assignee is None:
        raise TaskDomainException("DONE task requires assignee")

    old_status = task.status
    old_assignee = task.assignee

    if assignee_was_set:
        validate_task_assignment(
            task=task,
            assignee=dto.assignee,
            actor=actor,
        )

    for field, value in dto.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    task.save()

    if dto.status and dto.status != old_status:
        activity_service.log_field_change(
            task=task,
            actor=actor,
            field="status",
            old_value=old_status,
            new_value=dto.status,
            action=TaskActivity.Action.STATUS_CHANGED,
        )

    if assignee_was_set and old_assignee != dto.assignee:
        activity_service.log_field_change(
            task=task,
            actor=actor,
            field="assignee",
            old_value=old_assignee,
            new_value=dto.assignee,
            action=TaskActivity.Action.ASSIGNEE_CHANGED,
        )

    return task


def validate_task_assignment(*, task: Task, assignee, actor):
    board = task.board

    if not permission_service.can_assign_task(
        user=actor,
        board=board,
    ):
        raise TaskDomainException("You do not have permission to assign tasks")

    if assignee and assignee not in board.members.all():
        raise TaskDomainException("Assignee must be board member")


def assign_task(*, task: Task, assignee, actor):
    validate_task_assignment(
        task=task,
        assignee=assignee,
        actor=actor,
    )

    if task.status == Task.Status.DONE:
        raise TaskDomainException("Cannot assign user to DONE task")

    if task.assignee == assignee:
        return task

    old_assignee = task.assignee
    task.assignee = assignee
    task.save()

    activity_service.log_field_change(
        task=task,
        actor=actor,
        field="assignee",
        old_value=old_assignee,
        new_value=assignee,
        action=TaskActivity.Action.ASSIGNEE_CHANGED,
    )

    return task
