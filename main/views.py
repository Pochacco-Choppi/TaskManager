from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
import django_filters

from .models import User, Task, Tag
from .serializers import UserSerializer, TaskSerializer, TagSerializer
from .permissions import StaffPermissions


class UserFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = ("first_name",)


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Task.Status.choices)
    author = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    assignee = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Task
        fields = ("status", "author", "tags", "assignee")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter
    permission_classes = [StaffPermissions | DjangoModelPermissionsOrAnonReadOnly]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = (
        Task.objects.select_related("author", "assignee")
        .prefetch_related("tags")
        .order_by("priority")
    )
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    permission_classes = [StaffPermissions | DjangoModelPermissionsOrAnonReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer
    permission_classes = [StaffPermissions | DjangoModelPermissionsOrAnonReadOnly]
