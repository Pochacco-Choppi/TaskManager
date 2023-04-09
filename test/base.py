from typing import Union, List
from http import HTTPStatus

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from main.models import Tag, Task, User

IS_STAFF_IF_RUN = "IS_STAFF_IF_RUN"
IS_STAFF_ELSE_RUN = "IS_STAFF_ELSE_RUN"


class TestViewSetBase(APITestCase):
    client: APIClient
    admin: User
    basename: str
    users_to_test: List

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.admin = cls.create_api_superuser(
            {"username": "test", "password": None, "email": None}
        )

        cls.client = APIClient()
        cls.auth_token = "vy6G89ujJ9ujTR5vuo5wdea2"

        cls.login_authenticate(cls.admin)

        cls.users_to_test = [cls.admin]

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=[key])

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    @staticmethod
    def create_api_user(user_attributes):
        return User.objects.create(**user_attributes)

    @staticmethod
    def create_api_superuser(user_attributes):
        return User.objects.create_superuser(**user_attributes)

    @staticmethod
    def create_task(task_attributes):
        return Task.objects.create(**task_attributes)

    @staticmethod
    def create_tag(tag_attributes):
        return Tag.objects.create(**tag_attributes)

    @classmethod
    def login_authenticate(cls, user):
        cls.client.force_login(user)
        cls.client.force_authenticate(user, cls.auth_token)

    @classmethod
    def login(cls, user):
        cls.client.force_login(user)

    def authenticate(self, user):
        self.client.force_authenticate(user, self.auth_token)

    def list(self, args: List[Union[str, int]] = None, user=None):
        user = user if user else self.admin

        self.authenticate(user)

        response = self.client.get(self.list_url(args))
        return response

    def detail(self, args: List[Union[str, int]] = None, user=None):
        user = user if user else self.admin

        self.authenticate(user)

        response = self.client.get(self.detail_url(args))
        return response

    def post(self, data: dict, args: List[Union[str, int]] = None, user=None):
        user = user if user else self.admin
        self.authenticate(user)

        response = self.client.post(self.list_url(args), data=data)
        return response

    def patch(self, data: dict, args: List[Union[str, int]] = None, user=None):
        user = user if user else self.admin

        self.authenticate(user)

        response = self.client.patch(self.detail_url(args), data=data)
        return response

    def put(self, data: dict, args: List[Union[str, int]] = None, user=None):
        user = user if user else self.admin

        self.authenticate(user)

        response = self.client.put(self.detail_url(args), data=data)
        return response

    def delete(self, args: List[Union[str, int]] = None, user=None):
        user = user if user else self.admin

        self.authenticate(user)

        response = self.client.delete(self.detail_url(args))
        return response


class TestViewSetPermissionsBase(TestViewSetBase):
    view_set = None
    model = None
    cases_to_run = None
    test_data = None
    post_data = None
    put_data = None
    patch_data = None

    @classmethod
    def set_test_data(cls):
        raise NotImplemented

    @classmethod
    def set_post_data(cls):
        cls.set_test_data()

    @classmethod
    def set_put_data(cls):
        cls.set_test_data()

    @classmethod
    def set_patch_data(cls):
        cls.set_test_data()

    @classmethod
    def setUp(cls):
        cls.set_test_data()
        default_user = cls.create_api_user(
            {"username": "default_user", "email": "", "password": ""}
        )

        for _ in range(2):
            cls.create_tag({"title": f"Tag {_}"})

        for _ in range(2):
            cls.create_task(
                {
                    "title": f"Task {_}",
                    "deadline_date": "2022-12-12",
                    "description": "Some description",
                    "author": cls.admin,
                    "assignee": default_user,
                    "priority": 1,
                }
            )

        cls.users_to_test.append(default_user)

        cls.cases_to_run = {IS_STAFF_IF_RUN: False, IS_STAFF_ELSE_RUN: False}
        cls.model = cls.view_set.serializer_class.Meta.model

    @classmethod
    def assert_all_cases_run(cls):
        assert all(cls.cases_to_run.values()), (
            "Some cases doesn't runs check if "
            "cls.users_to_test has all needed users for test."
        )

    def assert_get_list(self):
        for user in self.users_to_test:
            # Check GET
            response = self.list(user=user)
            assert response.status_code == HTTPStatus.OK, response.content

    def assert_post_list(self):
        data = self.post_data if self.post_data else self.test_data
        db_object_count = self.model.objects.count()
        for user in self.users_to_test:
            # Check POST
            response = self.post(data, user=user)
            if user.is_staff:
                assert response.status_code == HTTPStatus.CREATED, response.content
                response = self.list(user=user)
                assert len(response.json()) == db_object_count + 1, response.json()
                self.cases_to_run[IS_STAFF_IF_RUN] = True
            else:
                assert response.status_code == HTTPStatus.FORBIDDEN, response.content
                self.cases_to_run[IS_STAFF_ELSE_RUN] = True

        self.assert_all_cases_run()

    def assert_get_detail(self):
        for user in self.users_to_test:
            # Check GET
            response = self.detail(args=self.model.objects.last().id, user=user)
            assert response.status_code == HTTPStatus.OK, response.content

    def assert_patch_detail(self):
        data = self.patch_data if self.patch_data else self.test_data
        for user in self.users_to_test:
            # Check PATH
            if user.is_staff:
                response = self.patch(
                    data,
                    args=self.model.objects.last().id,
                    user=user,
                )
                assert response.status_code == HTTPStatus.OK, response.content
                self.cases_to_run[IS_STAFF_IF_RUN] = True
            else:
                response = self.patch(
                    data,
                    args=self.model.objects.last().id,
                    user=user,
                )
                assert response.status_code == HTTPStatus.FORBIDDEN, response.content
                self.cases_to_run[IS_STAFF_ELSE_RUN] = True

        self.assert_all_cases_run()

    def assert_put_detail(self):
        data = self.put_data if self.put_data else self.test_data
        for user in self.users_to_test:
            # Check PUT
            if user.is_staff:
                response = self.put(
                    args=self.model.objects.last().id,
                    data=data,
                    user=user,
                )
                assert response.status_code == HTTPStatus.OK, response.content
                self.cases_to_run[IS_STAFF_IF_RUN] = True
            else:
                response = self.put(
                    args=self.model.objects.last().id,
                    data=data,
                    user=user,
                )
                assert response.status_code == HTTPStatus.FORBIDDEN, response.content
                self.cases_to_run[IS_STAFF_ELSE_RUN] = True
        self.assert_all_cases_run()

    def assert_delete_detail(self):
        db_object_count = self.model.objects.count()
        for user in self.users_to_test:
            self.authenticate(user)

            # Check DELETE
            if user.is_staff:
                response = self.delete(
                    args=self.model.objects.last().id,
                    user=user,
                )
                assert response.status_code == HTTPStatus.NO_CONTENT, response.content
                response = self.list(user=user)
                assert len(response.json()) == db_object_count - 1, response.json()
                self.cases_to_run[IS_STAFF_IF_RUN] = True
            else:
                response = self.delete(
                    args=self.model.objects.last().id,
                    user=user,
                )
                assert response.status_code == HTTPStatus.FORBIDDEN, response.content
                self.cases_to_run[IS_STAFF_ELSE_RUN] = True

        self.assert_all_cases_run()
