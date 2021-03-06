import pytest
from api.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import BlacklistedToken, RefreshToken


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

        data = response.data

        assert response.status_code == status.HTTP_201_CREATED
        assert data["created_on_holiday"] == {}
        assert data["email"] == user_data.email
        assert data["geo_data"] == user_data.geo_data
        assert data["username"] == user_data.username
        assert data["posts"] == []
        assert "password" not in data

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
        user_data.username = "????"
        response = api_client.post(
            self.endpoint, data=user_data.to_dict(), format="json"
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["username"] == user_data.username


@pytest.mark.django_db
class TestUserDetailView(object):
    def test_unauthorized_access(self, api_client, valid_user):
        url = reverse("user-detail", kwargs={"pk": valid_user.id})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_not_allowed(self, api_client_with_token, valid_user):
        url = reverse("user-detail", kwargs={"pk": valid_user.id})
        response = api_client_with_token.delete(url)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_post_not_allowed(self, api_client_with_token, valid_user):
        url = reverse("user-detail", kwargs={"pk": valid_user.id})
        response = api_client_with_token.post(url)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_put_not_allowed(self, api_client_with_token, valid_user):
        url = reverse("user-detail", kwargs={"pk": valid_user.id})
        response = api_client_with_token.put(url)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_get_user_details(
        self, api_client_with_token, valid_user, user_data
    ):
        url = reverse("user-detail", kwargs={"pk": valid_user.id})
        response = api_client_with_token.get(url)

        data = response.data

        assert response.status_code == status.HTTP_200_OK
        assert data["username"] == user_data.username
        assert data["email"] == user_data.email
        assert data["geo_data"] == user_data.geo_data
        assert len(data["posts"]) == 0

    def test_get_user_details_with_posts(
        self, api_client_with_token, valid_user, user_data, post
    ):
        url = reverse("user-detail", kwargs={"pk": valid_user.id})
        response = api_client_with_token.get(url)

        data = response.data

        assert response.status_code == status.HTTP_200_OK
        assert len(data["posts"]) == 1
        assert int(data["posts"][0].split("/")[-2]) == post.id

    def test_get_user_not_existing(self, api_client_with_token):
        url = reverse("user-detail", kwargs={"pk": 9999999999})
        response = api_client_with_token.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestPostDetailView(object):
    def test_unauthorized_access(self, api_client, valid_user):
        url = reverse("post-detail", kwargs={"pk": valid_user.id})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_not_allowed(self, api_client_with_token, post):
        url = reverse("post-detail", kwargs={"pk": post.id})
        response = api_client_with_token.delete(url)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_post_not_allowed(self, api_client_with_token, post):
        url = reverse("post-detail", kwargs={"pk": post.id})
        response = api_client_with_token.post(url)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_put_not_allowed(self, api_client_with_token, post):
        url = reverse("post-detail", kwargs={"pk": post.id})
        response = api_client_with_token.put(url)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_post_detail(
        self, api_client_with_token, post, post_data, valid_user
    ):
        url = reverse("post-detail", kwargs={"pk": post.id})
        response = api_client_with_token.get(url)

        data = response.data

        assert response.status_code == status.HTTP_200_OK
        assert data["content"] == post_data.content
        assert int(data["author"].split("/")[-2]) == valid_user.id
        assert len(data["likes"]) == 0


@pytest.mark.django_db
class TestLikesView(object):
    def test_unauthorized_access(self, api_client, post):
        url = reverse("likes", kwargs={"pk": post.id})
        response = api_client.put(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_not_allowed(self, api_client_with_token, post):
        url = reverse("likes", kwargs={"pk": post.id})
        response = api_client_with_token.delete(url)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_post_not_allowed(self, api_client_with_token, post):
        url = reverse("likes", kwargs={"pk": post.id})
        response = api_client_with_token.post(url)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_get_not_allowed(self, api_client_with_token, post):
        url = reverse("likes", kwargs={"pk": post.id})
        response = api_client_with_token.get(url)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_user_likes_a_post_adds_count(
        self, api_client_with_token, post, post_data
    ):
        likes_count_before = post.likes.count()
        url = reverse("likes", kwargs={"pk": post.id})
        response = api_client_with_token.put(
            url, data=post_data.to_dict(exclude=["author"]), format="json"
        )

        data = response.data

        assert len(data["likes"]) == likes_count_before + 1

    def test_user_likes_then_unlikes_a_post_resets_count(
        self, api_client_with_token, post, post_data
    ):
        likes_count_before = post.likes.count()
        url = reverse("likes", kwargs={"pk": post.id})
        api_client_with_token.put(
            url, data=post_data.to_dict(exclude=["author"]), format="json"
        )
        response = api_client_with_token.put(
            url, data=post_data.to_dict(exclude=["author"]), format="json"
        )

        data = response.data

        assert len(data["likes"]) == likes_count_before


@pytest.mark.django_db
class TestPostCreateView(object):
    endpoint = reverse("post-create")

    def test_unauthorized_access(self, api_client):
        response = api_client.post(self.endpoint)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_not_allowed(self, api_client_with_token):
        response = api_client_with_token.delete(self.endpoint)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_get_not_allowed(self, api_client_with_token):
        response = api_client_with_token.get(self.endpoint)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_put_not_allowed(self, api_client_with_token):
        response = api_client_with_token.put(self.endpoint)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_create_post_with_valid_data(
        self, api_client_with_token, post_data, valid_user
    ):
        response = api_client_with_token.post(
            self.endpoint,
            data=post_data.to_dict(exclude=["author"]),
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["content"] == post_data.content
        assert int(response.data["author"].split("/")[-2]) == valid_user.id

    def test_create_user_with_missing_email(
        self, api_client_with_token, post_data
    ):
        post_data.content = None
        response = api_client_with_token.post(
            self.endpoint,
            data=post_data.to_dict(exclude=["author"]),
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            str(response.data["content"][0]) == "This field may not be null."
        )


@pytest.mark.django_db
class TestLoginView(object):
    endpoint = reverse("login")

    def test_login_user_with_valid_credentials_with_access_token(
        self, api_client_with_token, user_data, valid_user
    ):
        credentials = {
            "username": user_data.username,
            "password": user_data.password,
        }
        response = api_client_with_token.post(
            self.endpoint, data=credentials, format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_user_with_valid_credentials_without_access_token(
        self, api_client, user_data, valid_user
    ):
        credentials = {
            "username": user_data.username,
            "password": user_data.password,
        }
        response = api_client.post(
            self.endpoint, data=credentials, format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_user_with_invalid_password(
        self, api_client_with_token, user_data, valid_user
    ):
        credentials = {
            "username": user_data.username,
            "password": "wrong password here",
        }
        response = api_client_with_token.post(
            self.endpoint, data=credentials, format="json"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_user_with_email_password(
        self, api_client_with_token, user_data, valid_user
    ):
        credentials = {
            "username": "fake@email.me",
            "password": user_data.username,
        }
        response = api_client_with_token.post(
            self.endpoint, data=credentials, format="json"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestLogoutView(object):
    endpoint = reverse("logout")

    def test_logout(self, api_client_with_token, user_data, valid_user):
        credentials = {
            "username": user_data.username,
            "password": user_data.password,
        }
        login_response = api_client_with_token.post(
            reverse("login"), data=credentials, format="json"
        )

        blacklist_count_before = BlacklistedToken.objects.count()
        response = api_client_with_token.post(
            self.endpoint,
            data={"refresh": login_response.data["refresh"]},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert BlacklistedToken.objects.count() == blacklist_count_before + 1
