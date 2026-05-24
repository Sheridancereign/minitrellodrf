from rest_framework import generics

from boards.models import Board, Task, TaskActivity
from boards.permissions import IsBoardOwner
from boards.serializers import BoardSerializer, TaskActivitySerializer, TaskSerializer


class BoardListCreateView(generics.ListCreateAPIView):
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(owner=self.request.user)


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
        ).select_related("board", "assignee", "created_by")


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(board__owner=self.request.user).select_related(
            "board",
            "assignee",
            "created_by",
        )


class TaskActivityListView(generics.ListAPIView):
    serializer_class = TaskActivitySerializer

    def get_queryset(self):
        return TaskActivity.objects.filter(
            task__board__owner=self.request.user
        ).select_related(
            "actor",
            "task",
        )
