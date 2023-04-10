from rest_framework import serializers

from .models import User, Task, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "date_of_birth",
            "phone",
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "id",
            "title",
        )


class TaskSerializer(serializers.ModelSerializer):
    tags = TagSerializer(
        many=True,
        read_only=True,
    )
    author = UserSerializer(
        read_only=True,
    )
    assignee = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "author",
            "assignee",
            "deadline_date",
            "status",
            "priority",
            "tags",
        )
