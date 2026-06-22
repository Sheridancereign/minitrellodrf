from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict

from boards.models import Board, Task
from users.models import User


class CreateTaskDTO(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    title: str
    description: Optional[str] = ""

    status: Task.Status = Task.Status.TODO
    priority: Task.Priority = Task.Priority.MEDIUM

    due_date: Optional[date] = None

    board: Board
    assignee: Optional[User] = None


class UpdateTaskDTO(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[date] = None
    assignee: Optional[User] = None
