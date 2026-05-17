from pygments.lexers import data
from rest_framework import serializers
from boards.models import Board, Task


class BoardSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Board
        fields = (
            "id",
            "title",
            "description",
            "owner",
            "created_at",
        )


class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

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


