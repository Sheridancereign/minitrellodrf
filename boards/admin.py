from django.contrib import admin

from boards.models import Board, BoardMembership, Task, TaskActivity


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "created_at")
    search_fields = ("title", "owner__username", "owner__email")
    list_filter = ("created_at",)


@admin.register(BoardMembership)
class BoardMembershipAdmin(admin.ModelAdmin):
    list_display = ("id", "board", "user", "created_at")
    search_fields = ("board__title", "user__username", "user__email")
    list_filter = ("created_at",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "board",
        "status",
        "priority",
        "assignee",
        "created_by",
        "due_date",
        "created_at",
    )
    search_fields = ("title", "board__title", "assignee__username")
    list_filter = ("status", "priority", "created_at", "due_date")


@admin.register(TaskActivity)
class TaskActivityAdmin(admin.ModelAdmin):
    list_display = ("id", "task", "action", "field", "actor", "created_at")
    search_fields = ("task__title", "actor__username", "field")
    list_filter = ("action", "created_at")
