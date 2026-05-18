from datetime import date

from boards.dto.task_dto import CreateTaskDTO, UpdateTaskDTO
from boards.exceptions import TaskDomainException
from boards.models import Task, TaskActivity
from boards.services.activity_service import (
    ActivityService,
)


class TaskService:
    @staticmethod
    def create_task(*, dto: CreateTaskDTO, user):
        board = dto.board

        if board.owner != user:
            raise TaskDomainException(
                "You are not the owner of this board"
            )

        if (
                dto.status == Task.Status.DONE
                and dto.assignee is None
        ):
            raise TaskDomainException(
                "Task cannot be DONE without assignee"
            )

        if (
                dto.due_date
                and dto.due_date < date.today()
        ):
            raise TaskDomainException(
                "Due date cannot be in the past"
            )

        if (
                dto.assignee
                and dto.assignee not in board.members.all()
        ):
            raise TaskDomainException(
                "Assignee must be board member"
            )

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

        ActivityService.log_task_created(
            task=task,
            actor=user,
        )

        return task

    @staticmethod
    def update_task(*, task: Task, dto: UpdateTaskDTO):

        if task.status == Task.Status.DONE:
            raise TaskDomainException(
                "Done tasks cannot be modified"
            )
        if (
                dto.due_date
                and dto.due_date < date.today()
        ):
            raise TaskDomainException(
                "Due date cannot be in the past"
            )

        next_status = dto.status or task.status

        next_assignee = (
            dto.assignee
            if dto.assignee is not None
            else task.assignee
        )

        if (
                next_status == Task.Status.DONE
                and next_assignee is None
        ):
            raise TaskDomainException(
                "DONE task requires assignee"
            )
        for field, value in dto.model_dump(
                exclude_unset=True
        ).items():
            setattr(task, field, value)

        if dto.status and dto.status != task.status:
            ActivityService.log_field_change(
                task=task,
                actor=task.created_by,
                field="status",
                old_value=task.status,
                new_value=dto.status,
                action=TaskActivity.Action.STATUS_CHANGED,
            )
        if (
                dto.assignee
                and dto.assignee != task.assignee
        ):
            ActivityService.log_field_change(
                task=task,
                actor=task.created_by,
                field="assignee",
                old_value=dto.assignee,
                new_value=dto.assignee,
                action=TaskActivity.Action.STATUS_CHANGED,
            )

        task.save()

        return task
