from http import HTTPStatus

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from main.models import Tag, Task, User
from main.views import TaskViewSet, UserViewSet, TagViewSet


class TestViewSetPermissions(APITestCase):
    client: APIClient
    admin: User
    default_user: User

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.admin = User.objects.create_superuser(
            "admin@test.ru", email=None, password="None"
        )
        cls.default_user = User.objects.create_user(
            "user@test.ru", email=None, password="None"
        )

        cls.user_to_delete = User.objects.create_user(
            "user_to_delete@test.ru", email=None, password="None"
        )

        cls.tag = Tag.objects.create(title="Hello I'm tag!")
        cls.tag_to_delete = Tag.objects.create(title="Hello I'm tag two!")
        cls.task = Task.objects.create(
            deadline_date="2023-04-12",
            priority=1,
            title="Hello task",
            description="Hello description",
        )
        cls.task.tags.set([cls.tag])

        cls.task_to_delete = Task.objects.create(
            deadline_date="2023-04-12",
            priority=1,
            title="Hello task",
            description="Hello description",
        )
        cls.task_to_delete.tags.set([cls.tag])

        cls.client = APIClient()
        cls.auth_token = "vy6G89ujJ9ujTR5vuo5wdea2"

        cls.users_count = User.objects.count()
        cls.users = [cls.admin, cls.default_user]

    @classmethod
    def assert_get_list(cls, view_set):
        model = view_set.serializer_class.Meta.model
        url = reverse(f"{model.__name__.lower()}s-list")
        for user in cls.users:
            # Check GET
            cls.client.force_authenticate(user, cls.auth_token)
            response = cls.client.get(url)
            assert response.status_code == HTTPStatus.OK, response.content

    @classmethod
    def assert_post_list(cls, view_set, post_data):
        model = view_set.serializer_class.Meta.model
        url = reverse(f"{model.__name__.lower()}s-list")
        db_object_count = model.objects.count()
        for user in cls.users:
            # Check POST
            cls.client.force_authenticate(user, cls.auth_token)
            response = cls.client.post(url, data=post_data)
            if user.is_staff:
                assert response.status_code == HTTPStatus.CREATED, response.content
                response = cls.client.get(url)
                assert len(response.json()) == db_object_count + 1, response.json()
            else:
                assert response.status_code == HTTPStatus.FORBIDDEN, response.content

    @classmethod
    def assert_get_patch_put_detail(cls, view_set, data):
        model = view_set.serializer_class.Meta.model
        url = reverse(
            f"{model.__name__.lower()}s-detail", args=str(model.objects.count())
        )
        for user in cls.users:
            # Check GET
            cls.client.force_authenticate(user, cls.auth_token)
            response = cls.client.get(url)
            assert response.status_code == HTTPStatus.OK, response.content

            # Check PATH
            if user.is_staff:
                response = cls.client.patch(url, data=data)
                assert response.status_code == HTTPStatus.OK, response.content
            else:
                response = cls.client.patch(url)
                assert response.status_code == HTTPStatus.FORBIDDEN, response.content
            # Check PUT
            if user.is_staff:
                response = cls.client.put(url, data=data)
                assert response.status_code == HTTPStatus.OK, response.content
            else:
                response = cls.client.put(url)
                assert response.status_code == HTTPStatus.FORBIDDEN, response.content

    @classmethod
    def assert_detail_delete(cls, view_set):
        model = view_set.serializer_class.Meta.model
        url_name = f"{model.__name__.lower()}s-detail"
        url = reverse(url_name, args=str(model.objects.count()))
        db_object_count = model.objects.count()
        for user in cls.users:
            cls.client.force_authenticate(user, cls.auth_token)

            # Check DELETE
            if user.is_staff:
                response = cls.client.delete(url)
                assert response.status_code == HTTPStatus.NO_CONTENT, response.content
                response = cls.client.get(reverse(f'{url_name.split("-")[0]}-list'))
                assert len(response.json()) == db_object_count - 1, response.json()
            else:
                response = cls.client.delete(url)
                assert response.status_code == HTTPStatus.FORBIDDEN, response.content

    def test_user_list(self) -> None:
        view_set = UserViewSet
        post_data = {
            "username": "test_user_name",
            "first_name": "test",
            "last_name": "test",
            "email": "test@tester.com",
            "date_of_birth": "",
            "phone": "",
        }

        self.assert_get_list(view_set)
        self.assert_post_list(view_set, post_data)

    def test_task_list(self) -> None:
        view_set = TaskViewSet
        post_data = {
            "deadline_date": "2023-04-12",
            "priority": 1,
            "title": "Hello task",
            "description": "Hello description",
            "tags": [self.tag.id],
        }
        self.assert_get_list(view_set)
        self.assert_post_list(view_set, post_data)

    def test_tag_list(self) -> None:
        view_set = TagViewSet
        post_data = {
            "title": "Hello tag",
        }
        self.assert_get_list(view_set)
        self.assert_post_list(view_set, post_data)

    def test_user_detail_get_patch_put(self):
        view_set = UserViewSet
        data = {
            "username": "test_user_name",
            "first_name": "test",
            "last_name": "test",
            "email": "test@tester.com",
            "date_of_birth": "",
            "phone": "",
        }

        self.assert_get_patch_put_detail(view_set, data)

    def test_tag_detail_get_patch_put(self):
        view_set = TagViewSet
        data = {
            "title": "Tag title",
        }

        self.assert_get_patch_put_detail(view_set, data)

    def test_task_detail_get_patch_put(self):
        view_set = TaskViewSet
        data = {
            "deadline_date": "2023-04-12",
            "priority": 1,
            "title": "Hello task",
            "description": "Hello description",
            "tags": [self.tag.id],
        }

        self.assert_get_patch_put_detail(view_set, data)

    def test_user_detail_delete(self):
        view_set = UserViewSet

        self.assert_detail_delete(view_set)

    def test_task_detail_delete(self):
        view_set = TaskViewSet

        self.assert_detail_delete(view_set)

    def test_tag_detail_delete(self):
        view_set = TagViewSet

        self.assert_detail_delete(view_set)
