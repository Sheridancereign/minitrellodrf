from rest_framework import serializers

from boards.dto.task_dto import CreateTaskDTO, UpdateTaskDTO
from boards.models import Board, BoardMembership, Task, TaskActivity
from boards.services import task_service


class BoardSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Board
        fields = (
            "id",
            "title",
            "description",
            "owner",
            "created_at",
        )

    def create(self, validated_data):
        user = self.context["request"].user

        board = Board.objects.create(owner=user, **validated_data)

        BoardMembership.objects.create(
            board=board,
            user=user,
            role=BoardMembership.Role.OWNER,
        )

        return board


class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = Task
        fields = (
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
        )

    def create(self, validated_data):
        user = self.context["request"].user

        dto = CreateTaskDTO(**validated_data)

        return task_service.create_task(
            dto=dto,
            user=user,
        )

    def update(self, instance, validated_data):
        user = self.context["request"].user

        dto = UpdateTaskDTO(**validated_data)

        return task_service.update_task(
            task=instance,
            dto=dto,
            actor=user,
        )


class TaskActivitySerializer(serializers.ModelSerializer):
    actor = serializers.ReadOnlyField(source="actor.username")

    class Meta:
        model = TaskActivity
        fields = (
            "id",
            "action",
            "field",
            "old_value",
            "new_value",
            "actor",
            "created_at",
        )
