from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Task, User
from rest_framework.views import APIView
from .serializers import TaskSerializer, AssignTaskSerializer

class CreateTaskView(generics.CreateAPIView, generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Task created successfully!",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssignTaskView(APIView):

    def post(self, request):
        serializer = AssignTaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            return Response(
                {
                    "message": "Task assigned successfully",
                    "task_id": task.id,
                    "assigned_users": [user.email for user in task.assigned_users.all()]
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        # Fetch all users with their emails and names
        users = User.objects.all().values('id', 'email', 'name')
        user_list = [
            {
                "id": user['id'],
                "name": user['name'],
                "email": user['email']
            }
            for user in users
        ]

        # Fetch all tasks with their IDs and names
        tasks = Task.objects.all().values('id', 'name')
        task_list = [
            {
                "id": task['id'],
                "name": task['name']
            }
            for task in tasks
        ]

        return Response(
            {
                "users": user_list,
                "tasks": task_list
            },
            status=status.HTTP_200_OK
        )
