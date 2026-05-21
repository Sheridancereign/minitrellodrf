from django.urls import path

from boards.views import (
    BoardDetailView,
    BoardListCreateView,
    TaskActivityListView,
    TaskDetailView,
    TaskListCreateView,
)

urlpatterns = [
    path("", BoardListCreateView.as_view(), name="boards"),
    path("<int:pk>/", BoardDetailView.as_view(), name="board-detail"),
    path("tasks/", TaskListCreateView.as_view(), name="task-list"),
    path("<int:pk>/tasks/", TaskDetailView.as_view(), name="task-detail"),
    path("activities/", TaskActivityListView.as_view(), name="activity-list"),
]
