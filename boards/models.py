from django.conf import settings
from django.db import models


class Board(models.Model):
    title = models.CharField(max_length=120)

    description = models.TextField(
        blank=True,
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owner_boards",
    )

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="members_boards",
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Task(models.Model):
    class Status(models.TextChoices):
        TODO = "TODO", "To do"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        DONE = "DONE", "Done"

    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"

    title = models.CharField(max_length=120)

    description = models.TextField(
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO,
    )

    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )

    due_date = models.DateField(
        blank=True,
        null=True,
    )

    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name="tasks",
    )

    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="assigned_tasks",
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_tasks",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TaskActivity(models.Model):
    class Action(models.TextChoices):
        CREATED = (
            "CREATED",
            "Created",
        )
        STATUS_CHANGED = (
            "STATUS_CHANGED",
            "Status Changed",
        )
        ASSIGNEE_CHANGED = (
            "ASSIGNEE_CHANGED",
            "Assignee Changed",
        )
        UPDATED = "UPDATED", "Updated"

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="activities",
    )

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    action = models.CharField(
        max_length=20,
        choices=Action.choices,
    )

    field = models.CharField(
        max_length=20,
        choices=Action.choices,
    )

    old_value = models.CharField(
        blank=True,
    )
    new_value = models.CharField(
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} - {self.task.title}"
