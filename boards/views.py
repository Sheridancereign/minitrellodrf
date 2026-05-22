from rest_framework import generics

from boards.dto.task_dto import CreateTaskDTO, UpdateTaskDTO
from boards.models import Board, BoardMembership, Task, TaskActivity
from boards.permissions import IsBoardOwner
from boards.serializers import BoardSerializer, TaskActivitySerializer, TaskSerializer
from boards.services import task_service


class BoardListCreateView(generics.ListCreateAPIView):
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(
            owner=self.request.user
        )

    def perform_create(self, serializer):
        board = serializer.save(
            owner=self.request.user
        )

        BoardMembership.objects.create(
            user=self.request.user,
            board=board,
            role=BoardMembership.Role.OWNER,
        )


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BoardSerializer
    permission_classes = [IsBoardOwner]

    def get_queryset(self):
        return Board.objects.filter(owner=self.request.user)


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(
            board__owner=self.request.user,
        ).select_related('board', 'assignee', "created_by")

    def perform_create(self, serializer):
        dto = CreateTaskDTO(
            **serializer.validated_data
        )

        task = task_service.create_task(
            dto=dto,
            user=self.request.user,
        )

        serializer.instance = task


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(
            board__owner=self.request.user
        ).select_related(
            "board",
            "assignee",
            "created_by",
        )

    def perform_update(self, serializer):
        dto = UpdateTaskDTO(
            **serializer.validated_data
        )

        task = task_service.update_task(
            task=self.get_object(),
            dto=dto,
            actor=self.request.user,
        )

        serializer.instance = task


class TaskActivityListView(generics.ListAPIView):
    serializer_class = TaskActivitySerializer

    def get_queryset(self):
        return TaskActivity.objects.filter(
            task__board__owner=self.request.user
        ).select_related(
            "actor",
            "task",
        )
