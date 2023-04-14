from http import HTTPStatus

from main.views import TaskViewSet, UserViewSet, TagViewSet
from test.base import TestViewSetAPIBase


class TestUserViewSet(TestViewSetAPIBase):
    basename = "users"
    view_set = UserViewSet

    @classmethod
    def set_test_data(cls):
        cls.test_data = {
            'username': 'johnsmith',
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'john@test.com',
            'date_of_birth': '2000-01-01',
            'phone': '+79000000000',
        }
        cls.put_data = {
            'username': 'tralala',
            'first_name': 'Dadada',
            'last_name': 'Smith',
            'email': 'john@test.com',
            'date_of_birth': '2000-01-01',
            'phone': '+79000000000',
        }
        cls.patch_data = {
            'username': 'Drida',
            'last_name': 'Trithththt',
            'email': 'puted_mail@test.com',
        }

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_post(self):
        response = self.post(self.test_data)
        expected_response = self.expected_details(response.data, self.test_data)
        assert response.status_code == HTTPStatus.OK, response.content
        assert response.data == expected_response

    def test_put(self):
        response = self.put(self.put_data, args=self.default_user.id)
        expected_response = self.expected_details(response.data, self.put_data)
        assert response.status_code == HTTPStatus.OK, response.content
        assert response.data == expected_response

    def test_delete(self):
        response = self.delete(args=self.default_user.id)
        assert response.status_code == HTTPStatus.NO_CONTENT
