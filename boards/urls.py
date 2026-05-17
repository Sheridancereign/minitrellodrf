from django.urls import path

from boards.views import BoardListCreateView, BoardDetailView, TaskListCreateView, TaskDetailView

urlpatterns = [
    path("", BoardListCreateView.as_view(), name="boards"),
    path( "<int:pk>/",BoardDetailView.as_view(),name="board-detail",
    ),
    path("tasks/", TaskListCreateView.as_view()),
    path("<int:pk>/tasks/", TaskDetailView.as_view()),
]