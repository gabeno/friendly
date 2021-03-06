import pytest
from api.models import Post, User
from api.tests import PostData, UserData
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def now():
    return timezone.now()


@pytest.fixture
def user_data():
    return UserData(
        username="@gm",
        email="gm@example.com",
        password="secure不",
        geo_data=dict(latitude=36.8155, longitude=-1.2841, ip="0.0.0.0"),
    )


@pytest.fixture
def post_data(valid_user):
    content = """Once upon a tyne, there lived a great old fellow who had
an amazing ability to see yonder!

He led a simple life back at the village. He was quite a honorable
person and very respected amongst his peers.

Abrupt end of story 😶 !!"""
    return PostData(author=valid_user, content=content)


@pytest.fixture
def valid_user(now, user_data):
    user = User(
        username=user_data.username,
        email=user_data.email,
        created_when=now,
        geo_data=user_data.geo_data,
    )
    user.set_password(user_data.password)
    user.save()
    return user


@pytest.fixture
def post(post_data, now, valid_user):
    return Post.objects.create(
        content=post_data.content,
        created_when=now,
        author=valid_user,
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_client_with_token(valid_user):
    client = APIClient()
    refresh = RefreshToken.for_user(valid_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client
