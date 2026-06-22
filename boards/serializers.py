from django.contrib.auth import get_user_model
from rest_framework import serializers

from boards.dto.task_dto import CreateTaskDTO, UpdateTaskDTO
from boards.models import Board, BoardMembership, Task, TaskActivity
from boards.services import board_service, task_service

user_model = get_user_model()


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

        try:
            return task_service.create_task(
                dto=dto,
                user=user,
            )
        except ValueError as exc:
            raise serializers.ValidationError({"detail": str(exc)}) from exc

    def update(self, instance, validated_data):
        user = self.context["request"].user

        dto = UpdateTaskDTO(**validated_data)

        try:
            return task_service.update_task(
                task=instance,
                dto=dto,
                actor=user,
            )
        except ValueError as exc:
            raise serializers.ValidationError({"detail": str(exc)}) from exc


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


class AssignTaskSerializer(serializers.Serializer):
    assignee = serializers.PrimaryKeyRelatedField(
        queryset=user_model.objects.all(),
        allow_null=True,
        required=True,
    )


class BoardMemberAssignSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=user_model.objects.all(),
        required=True,
    )

    def create(self, validated_data):
        request = self.context["request"]
        board = self.context["board"]

        try:
            return board_service.assign_board_member(
                board=board,
                user=validated_data["user"],
                actor=request.user,
            )
        except ValueError as exc:
            raise serializers.ValidationError({"detail": str(exc)}) from exc


class BoardMembershipSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = BoardMembership
        fields = (
            "id",
            "user",
            "created_at",
        )
