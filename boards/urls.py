from django.urls import path

from boards.views import (
    BoardDetailView,
    BoardListCreateView,
    BoardMemberAssignView,
    TaskActivityListView,
    TaskAssignView,
    TaskDetailView,
    TaskListCreateView,
)

app_name = "boards"

urlpatterns = [
    path("", BoardListCreateView.as_view(), name="boards"),
    path("<int:pk>/", BoardDetailView.as_view(), name="board-detail"),
    path(
        "<int:pk>/members/assign/",
        BoardMemberAssignView.as_view(),
        name="board-member-assign",
    ),
    path("tasks/", TaskListCreateView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/assign/", TaskAssignView.as_view(), name="task-assign"),
    path("activities/", TaskActivityListView.as_view(), name="activities"),
]
