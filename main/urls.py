from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet, TaskViewSet, TagViewSet

router = routers.SimpleRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"tasks", TaskViewSet, basename="tasks")
router.register(r"tags", TagViewSet, basename="tags")

urlpatterns = [
    path("api/", include(router.urls)),
]
