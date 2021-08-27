import pytest
from api.models import Post, User
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.utils import timezone

NOW = timezone.now()


@pytest.mark.django_db
class TestPostModel(object):
    def test_post_create_details_ok(self):
        content = """Once upon a tyne, there lived a great old fellow who had
an amazing ability to see yonder!

He led a simple life back at the village. He was quite a honorable
person and very respected amongst his peers.

Abrupt end of story 😶 !!"""

        post = Post.objects.create(
            content=content,
            created_when=NOW,
        )

        assert post.content == content
        assert post.created_when == NOW
        assert post.likes_count == 0
        assert post.author_id == 99

    def test_create_one_post_count_ok(self):
        before_count = Post.objects.count()
        Post.objects.create(
            content="content",
        )

        assert Post.objects.count() == before_count + 1

    def test_post_add_like_increases_count(self):
        p = Post.objects.create(
            content="content",
        )
        likes_count_before = p.likes_count
        p.likes_count += 1
        p.save()

        assert p.likes_count == likes_count_before + 1

    def test_create_multiple_posts_count_ok(self):
        before_count = Post.objects.count()
        Post.objects.create(
            content="content 1",
        )
        Post.objects.create(
            content="content 2",
        )

        assert Post.objects.count() == before_count + 2

    def test_delete_post_ok(self):
        p = Post.objects.create(
            content="content",
        )
        before_count = Post.objects.count()
        p.delete()

        assert Post.objects.count() == before_count - 1

    def test_create_post_with_empty_string_raises(self):
        with pytest.raises(ValidationError) as exec_info:
            Post.objects.create(content="")

        assert "This field cannot be blank" in str(exec_info)


@pytest.mark.django_db
class TestUserModel(object):
    def test_create_user_with_given_details(self):
        password = "secure不"
        hashed_password = User.hash_password(password)
        geo_data = dict(latitude=36.8155, longitude=-1.2841, ip="0.0.0.0")
        user = User(
            username="@gm",
            email="g@m.com",
            created_when=NOW,
            geo_data=dict(latitude=36.8155, longitude=-1.2841, ip="0.0.0.0"),
        )
        user.password = hashed_password
        user.save()

        assert user.username == "@gm"
        assert user.email == "g@m.com"
        assert user.created_when == NOW
        assert user.check_password(password) is True
        assert user.geo_data == geo_data

    def test_create_user_with_unique_username(self):
        with pytest.raises(ValidationError) as exec_info:
            User.objects.create(username="gm", email="g@m.com", password="123")
            User.objects.create(username="gm", email="m@g.com", password="123")
        assert "User with this Username already exists" in str(exec_info)

    def test_create_user_with_emoji_username(self):
        user = User.objects.create(
            username="😜", email="g@m.com", password="123"
        )

        assert user.username == "😜"

    def test_create_user_with_unique_email(self):
        with pytest.raises(ValidationError) as exec_info:
            User.objects.create(username="gm", email="g@m.com", password="123")
            User.objects.create(username="mg", email="g@m.com", password="123")
        assert "User with this Email already exists" in str(exec_info)

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
    def test_create_user_with_invalid_email(self, invalid_email):
        with pytest.raises(ValidationError) as exec_info:
            User.objects.create(username="gm", email=invalid_email)
        assert "Enter a valid email address" in str(exec_info)

    def test_check_wrong_password(self):
        hashed_password = User.hash_password("yes")
        user = User(
            username="@gm",
            email="g@m.com",
            created_when=NOW,
        )
        user.password = hashed_password
        user.save()

        assert user.check_password("no") is False

    def test_create_user_with_default_geo_data(self):
        hashed_password = User.hash_password("yes")
        user = User(
            username="u",
            email="g@m.com",
            created_when=NOW,
        )
        user.password = hashed_password
        user.save()

        assert user.geo_data == {}
