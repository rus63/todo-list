from http import HTTPStatus

from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import Token, RefreshToken

from todo.models import User


class TestViewSetBase(APITestCase):
    api_client = APIClient()
    base_name: str
    pagination: bool = False

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        user = User.objects.create_user(
            email="test@test.com", first_name="Will", last_name="Smith"
        )
        refresh = RefreshToken.for_user(user)
        cls.api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    @classmethod
    def detail_url(cls, key: int | str) -> str:
        return reverse(f"{cls.base_name}-detail", args=[key])

    @classmethod
    def list_url(cls, args: list[str | int] | None = None) -> str:
        return reverse(f"{cls.base_name}-list", args=args)

    def request_create(
        self,
        data: dict,
        args: list[str | int] | None = None,
        format_type: str | None = None,
        user: User | None = None,
    ) -> Response:
        return self.api_client.post(
            self.list_url(args), data=data, format_type=format_type, user=user
        )

    def create(
        self,
        data: dict,
        args: list[str | int] | None = None,
        user: User | None = None,
    ) -> dict:
        response = self.request_create(data, args, user=user)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data()

    def request_retrieve(self, entity: dict, user: User | None = None) -> Response:
        url = self.detail_url(entity["id"])
        return self.api_client.get(path=url, user=user)

    def retrieve(self, entity: dict, user: User | None = None) -> dict:
        response = self.request_retrieve(entity, user)
        assert response.status_code == HTTPStatus.OK
        return response.json()

    def request_update(
        self, entity: dict, attributes: dict, user: User | None = None
    ) -> Response:
        url = self.detail_url(entity["id"])
        return self.api_client.put(url, attributes, user=user)

    def update(self, entity: dict, attributes: dict, user: User | None = None) -> dict:
        response = self.request_update(entity, attributes, user)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.json()

    def request_partial_update(
        self, entity: dict, attributes: dict, user: User | None = None
    ) -> Response:
        url = self.detail_url(entity["id"])
        return self.api_client.patch(url, data=attributes, user=user)

    def partial_update(self, entity: dict, attributes: dict) -> dict:
        response = self.request_partial_update(entity, attributes)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.json()

    def delete(self, entity: dict, user: User | None = None) -> None:
        url = self.detail_url(entity["id"])
        response = self.api_client.delete(path=url, user=user)
        assert response.status_code == HTTPStatus.NO_CONTENT

    @classmethod
    def _assert_pagination(cls, response_json: dict) -> None:
        results = response_json["results"]
        assert response_json == {
            "count": len(results),
            "next": None,
            "previous": None,
            "results": results,
        }

    @classmethod
    def _assert_no_pagination(cls, response_json: dict) -> None:
        assert list(response_json.keys()) == ["results"]

    def request_list(self, data: dict = None, user: User | None = None) -> Response:
        return self.api_client.get(self.list_url(), data=data, user=user)

    def list(self, data: dict = None, user: User | None = None) -> list[dict]:
        response = self.request_list(data, user=user)
        assert response.status_code == HTTPStatus.OK, response.content

        if self.pagination:
            self._assert_pagination(response.json())
        else:
            self._assert_no_pagination(response.json())
        return response.json()["results"]
