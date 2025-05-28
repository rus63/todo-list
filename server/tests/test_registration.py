from http import HTTPStatus

from tests.base.test_base import TestViewSetBase
from todo.models import User


class TestUserRegistrationViewSet(TestViewSetBase):
    base_name = "registration"

    def test_register_user(self) -> None:
        attr = {
            "email": "ex@example.com",
            "password": "Testuser123",
            "password2": "Testuser123",
            "first_name": "Johny",
            "last_name": "Depp",
        }

        response = self.create(attr)

        created_user_obj = User.objects.get(id=response["id"])
        assert response == self.get_expected_user_detail(created_user_obj)

    def test_password_mismatch(self) -> None:
        attr = {
            "email": "ex@example.com",
            "password": "Testuser12",
            "password2": "Testuser123",
            "first_name": "Jason",
            "last_name": "Statham",
        }

        response = self.request_create(attr)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {"password": ["Passwords don't match."]}

    def get_expected_user_detail(self, user: User) -> dict:
        return {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
