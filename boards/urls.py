from django.urls import path

from boards.views import (
    BoardDetailView,
    BoardListCreateView,
    TaskActivityListView,
    TaskDetailView,
    TaskListCreateView,
)

app_name = "boards"

urlpatterns = [
    path("", BoardListCreateView.as_view(), name="boards"),
    path("<int:pk>/", BoardDetailView.as_view(), name="board-detail"),
    path("tasks/", TaskListCreateView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("activities/", TaskActivityListView.as_view(), name="activities"),
]
