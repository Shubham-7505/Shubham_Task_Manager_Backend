from rest_framework import serializers
from .models import Task, User

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['name', 'description']  # Only include name and description

class TaskAssignSerializer(serializers.ModelSerializer):
    assigned_users = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, required=False
    )

    class Meta:
        model = Task
        fields = ['id', 'assigned_users']

class AssignTaskSerializer(serializers.Serializer):
    task_id = serializers.IntegerField()
    emails = serializers.ListField(
        child=serializers.EmailField()
    )

    def validate(self, data):
        task_id = data.get('task_id')
        emails = data.get('emails')

        # Check if task exists
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise serializers.ValidationError({"task_id": "Task does not exist."})

        # Check if users exist
        users = User.objects.filter(email__in=emails)
        if not users.exists():
            raise serializers.ValidationError({"emails": "No users found with provided emails."})

        data['task'] = task
        data['users'] = users
        return data

    def create(self, validated_data):
        task = validated_data['task']
        users = validated_data['users']

        for user in users:
        # Assign task to user (updates User table)
            user.tasks.add(task)  
            user.save()

        return task
