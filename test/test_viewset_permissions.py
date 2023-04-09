from main.views import TaskViewSet, UserViewSet, TagViewSet
from test.base import TestViewSetPermissionsBase


class TestUserViewSetPermissions(TestViewSetPermissionsBase):
    view_set = UserViewSet
    basename = "users"

    @classmethod
    def set_test_data(cls):
        test_data = {
            "username": "test_user_name",
            "first_name": "test",
            "last_name": "test",
            "email": "test@tester.com",
            "date_of_birth": "",
            "phone": "",
        }
        cls.test_data = test_data

    def test_get_user_list(self) -> None:
        self.assert_get_list()

    def test_post_user_list(self) -> None:
        self.assert_post_list()

    def test_user_detail_delete(self):
        self.assert_delete_detail()

    def test_user_detail_put(self):
        self.assert_put_detail()

    def test_user_detail_patch(self):
        self.assert_put_detail()

    def test_user_detail_get(self):
        self.assert_get_detail()


class TestTaskViewSetPermission(TestViewSetPermissionsBase):
    view_set = TaskViewSet
    basename = "tasks"

    @classmethod
    def set_test_data(cls):
        tag = cls.create_tag({"title": "Hello world!"})
        test_data = {
            "deadline_date": "2023-04-12",
            "priority": 1,
            "title": "Hello task",
            "description": "Hello description",
            "tags": [tag.id],
        }
        cls.test_data = test_data

    def test_get_task_list(self) -> None:
        self.assert_get_list()

    def test_post_task_list(self) -> None:
        self.assert_post_list()

    def test_task_detail_delete(self):
        self.assert_delete_detail()

    def test_task_detail_put(self):
        self.assert_put_detail()

    def test_task_detail_patch(self):
        self.assert_put_detail()

    def test_task_detail_get(self):
        self.assert_get_detail()


class TestTagViewSetPermission(TestViewSetPermissionsBase):
    view_set = TagViewSet
    basename = "tags"

    @classmethod
    def set_test_data(cls):
        test_data = {
            "title": "New Tag!",
        }
        cls.test_data = test_data

    def test_get_tag_list(self) -> None:
        self.assert_get_list()

    def test_post_tag_list(self) -> None:
        self.assert_post_list()

    def test_tag_detail_delete(self):
        self.assert_delete_detail()

    def test_tag_detail_put(self):
        self.assert_put_detail()

    def test_tag_detail_patch(self):
        self.assert_put_detail()

    def test_tag_detail_get(self):
        self.assert_get_detail()
