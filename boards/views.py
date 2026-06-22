from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from boards.models import Board, Task, TaskActivity
from boards.permissions import IsBoardOwner
from boards.serializers import (
    AssignTaskSerializer,
    BoardMemberAssignSerializer,
    BoardMembershipSerializer,
    BoardSerializer,
    TaskActivitySerializer,
    TaskSerializer,
)
from boards.services import permission_service, task_service


@extend_schema(tags=["Boards"])
class BoardListCreateView(generics.ListCreateAPIView):
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(members=self.request.user)


@extend_schema(tags=["Boards"])
class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BoardSerializer
    permission_classes = [IsBoardOwner]

    def get_queryset(self):
        return Board.objects.filter(members=self.request.user)


@extend_schema(tags=["Boards"])
class BoardMemberAssignView(generics.GenericAPIView):
    serializer_class = BoardMemberAssignSerializer

    def get_queryset(self):
        if permission_service.can_manage_board_members(user=self.request.user):
            return Board.objects.all()

        return Board.objects.filter(
            members=self.request.user,
        ).distinct()

    def post(self, request, pk):
        board = self.get_object()
        serializer = self.get_serializer(
            data=request.data,
            context={
                **self.get_serializer_context(),
                "board": board,
            },
        )
        serializer.is_valid(raise_exception=True)
        membership = serializer.save()

        output_serializer = BoardMembershipSerializer(membership)

        return Response(
            output_serializer.data,
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["Tasks"])
class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(
            board__members=self.request.user,
        ).select_related("board", "assignee", "created_by")


@extend_schema(tags=["Tasks"])
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(board__members=self.request.user).select_related(
            "board",
            "assignee",
            "created_by",
        )


@extend_schema(tags=["Tasks"])
class TaskAssignView(generics.GenericAPIView):
    serializer_class = AssignTaskSerializer

    def get_queryset(self):
        if permission_service.can_assign_task(user=self.request.user):
            return Task.objects.all().select_related(
                "board",
                "assignee",
                "created_by",
            )

        return (
            Task.objects.filter(
                board__members=self.request.user,
            )
            .select_related(
                "board",
                "assignee",
                "created_by",
            )
            .distinct()
        )

    def post(self, request, pk):
        task = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            task = task_service.assign_task(
                task=task,
                assignee=serializer.validated_data["assignee"],
                actor=request.user,
            )
        except ValueError as exc:
            raise ValidationError({"detail": str(exc)}) from exc

        output_serializer = TaskSerializer(
            task,
            context=self.get_serializer_context(),
        )

        return Response(
            output_serializer.data,
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["Activities"])
class TaskActivityListView(generics.ListAPIView):
    serializer_class = TaskActivitySerializer

    def get_queryset(self):
        return TaskActivity.objects.filter(
            task__board__owner=self.request.user
        ).select_related(
            "actor",
            "task",
        )
