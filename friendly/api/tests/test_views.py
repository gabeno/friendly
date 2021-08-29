import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
class TestUserCreateView(object):
    endpoint = reverse("user-create")

    def test_delete_not_allowed(self, api_client):
        response = api_client.delete(self.endpoint)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_get_not_allowed(self, api_client):
        response = api_client.get(self.endpoint)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_put_not_allowed(self, api_client):
        response = api_client.put(self.endpoint)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_create_user_with_valid_data(self, api_client, user_data):
        response = api_client.post(
            self.endpoint, data=user_data.to_dict(), format="json"
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == user_data.to_dict(exclude=["password"])

    def test_create_user_with_missing_email(self, api_client, user_data):
        user_data.email = None
        response = api_client.post(
            self.endpoint, data=user_data.to_dict(), format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert str(response.data["email"][0]) == "This field may not be null."

    def test_create_user_with_unique_email(
        self, api_client, user_data, valid_user
    ):
        response = api_client.post(
            self.endpoint, data=user_data.to_dict(), format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            str(response.data["email"][0])
            == "user with this email already exists."
        )

    @pytest.mark.parametrize(
        "invalid_email",
        [
            ("user1", "name"),
            ("user2", "na.me"),
            ("user3", "@name"),
            ("user4", "@nam.e"),
            ("user5", "me@name.c"),
        ],
    )
    def test_create_user_with_invalid_email(
        self, api_client, invalid_email, user_data
    ):
        user_data.email = invalid_email
        response = api_client.post(
            self.endpoint, data=user_data.to_dict(), format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert str(response.data["email"][0]) == "Enter a valid email address."

    def test_create_user_with_missing_username(self, api_client, user_data):
        user_data.username = None
        response = api_client.post(
            self.endpoint, data=user_data.to_dict(), format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            str(response.data["username"][0]) == "This field may not be null."
        )

    def test_create_user_with_unique_username(
        self, api_client, user_data, valid_user
    ):
        response = api_client.post(
            self.endpoint, data=user_data.to_dict(), format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            str(response.data["username"][0])
            == "user with this username already exists."
        )

    def test_create_user_with_unicode_characters(self, api_client, user_data):
        user_data.username = "😜"
        response = api_client.post(
            self.endpoint, data=user_data.to_dict(), format="json"
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["username"] == user_data.username
