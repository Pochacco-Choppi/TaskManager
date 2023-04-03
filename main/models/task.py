from django.db import models

from .user import User
from .tag import Tag


class Task(models.Model):
    class Status(models.TextChoices):
        NEW = "new_task"
        IN_DEVELOPMENT = "in_development"
        IN_QA = "in_qa"
        IN_CODE_REVIEW = "in_code_review"
        READY_FOR_RELEASE = "ready_for_release"
        RELEASED = "released"
        ARCHIVED = "archived"

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="task_author"
    )
    assignee = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="task_assignee"
    )
    creation_date = models.DateField(auto_now_add=True)
    change_date = models.DateField(auto_now=True)
    deadline_date = models.DateField()
    status = models.CharField(
        max_length=255, default=Status.NEW, choices=Status.choices
    )
    priority = models.FloatField()
    tags = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
