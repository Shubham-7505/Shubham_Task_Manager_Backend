# Generated by Django 2.2.9 on 2025-03-26 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskManager', '0003_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='assigned_users',
        ),
        migrations.AddField(
            model_name='user',
            name='tasks',
            field=models.ManyToManyField(blank=True, related_name='assigned_users', to='taskManager.Task'),
        ),
    ]
