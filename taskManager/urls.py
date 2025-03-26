from django.urls import path
from .views import CreateTaskView, AssignTaskView

urlpatterns = [
    path('tasks/create/', CreateTaskView.as_view(), name='create-task'),
    path('task/assign/', AssignTaskView.as_view(), name='assign-task'),
]
