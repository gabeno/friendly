import pytest
from api.models import Post, User
from api.tests import PostData, UserData
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError


@pytest.mark.django_db
class TestPostModel(object):
    def test_post_create_details_ok(self, now, valid_user, post_data, post):
        assert post.content == post_data.content
        assert post.created_when == now
        assert post.likes_count == post_data.likes_count
        assert post.author == valid_user

    def test_create_one_post_count_ok(self, post_data):
        before_count = Post.objects.count()
        Post.objects.create(**post_data.to_dict())

        assert Post.objects.count() == before_count + 1

    def test_post_add_like_increases_count(self, post):
        likes_count_before = post.likes_count
        post.likes_count += 1
        post.save()

        assert post.likes_count == likes_count_before + 1

    def test_post_like_count_takes_only_positive_numbers(self, post):
        with pytest.raises(ValidationError) as exec_info:
            likes_count_before = post.likes_count
            post.likes_count -= 1
            post.save()

            assert likes_count_before == 0
            assert (
                "likes_count"
                and "Ensure this value is greater than or equal to 0"
                in str(exec_info)
            )

    def test_decrease_likes_count(self, post):
        likes_count_before = post.likes_count
        post.likes_count += 1
        post.save()

        assert likes_count_before == 0
        assert post.likes_count == likes_count_before + 1

    def test_create_multiple_posts_count_ok(self, post_data, post):
        before_count = Post.objects.count()
        Post.objects.create(**post_data.to_dict())

        assert Post.objects.count() == before_count + 1

    def test_delete_post_ok(self, post):
        before_count = Post.objects.count()
        post.delete()

        assert Post.objects.count() == before_count - 1

    def test_create_post_with_empty_string_raises(self, post_data):
        with pytest.raises(ValidationError) as exec_info:
            post_data.content = ""
            Post.objects.create(**post_data.to_dict())

        assert "content" and "This field cannot be blank" in str(exec_info)

    def test_create_post_without_author_raises(self, post_data):
        with pytest.raises(ValidationError) as exec_info:
            post_data.author = None
            Post.objects.create(**post_data.to_dict())

        assert "author" and "This field cannot be null" in str(exec_info)


@pytest.mark.django_db
class TestUserModel(object):
    def test_create_user_with_given_details(self, valid_user, now, user_data):
        assert valid_user.username == user_data.username
        assert valid_user.email == user_data.email
        assert valid_user.created_when == now
        assert valid_user.geo_data == user_data.geo_data
        assert valid_user.posts.count() == 0
        assert valid_user.password != user_data.password

    def test_create_user_without_email_raises(self, user_data):
        with pytest.raises(ValidationError) as exec_info:
            user_data.email = None
            User.objects.create(**user_data.to_dict())
        assert "This field cannot be null" in str(exec_info)

    def test_create_user_with_unique_username(self, user_data, valid_user):
        with pytest.raises(ValidationError) as exec_info:
            User.objects.create(**user_data.to_dict())
        assert "User with this Username already exists" in str(exec_info)

    def test_create_user_without_username_raises(self, user_data):
        with pytest.raises(ValidationError) as exec_info:
            user_data.username = None
            User.objects.create(**user_data.to_dict())
        assert "This field cannot be null" in str(exec_info)

    def test_create_user_with_emoji_username(self, user_data):
        user_data.username = "😜"
        user = User.objects.create(**user_data.to_dict())

        assert user.username == "😜"

    def test_create_user_with_unique_email(self, user_data, valid_user):
        with pytest.raises(ValidationError) as exec_info:
            User.objects.create(**user_data.to_dict())
        assert "User with this Email already exists" in str(exec_info)

    @pytest.mark.parametrize(
        "username,invalid_email",
        [
            ("user1", "name"),
            ("user2", "na.me"),
            ("user3", "@name"),
            ("user4", "@nam.e"),
            ("user5", "me@name.c"),
        ],
    )
    def test_create_user_with_invalid_email(
        self, username, invalid_email, user_data
    ):
        with pytest.raises(ValidationError) as exec_info:
            user_data.email = invalid_email
            user_data.username = username
            User.objects.create(**user_data.to_dict())
        assert "Enter a valid email address" in str(exec_info)

    def test_create_user_with_default_geo_data(self, user_data):
        user = User.objects.create(**user_data.to_dict(exclude=["geo_data"]))

        assert user.geo_data == {}

    def test_create_user_with_default_holiday_data(self, user_data):
        user = User.objects.create(**user_data.to_dict())

        assert user.created_on_holiday == {}

    def test_can_get_posts_for_author(self, post, valid_user):
        assert valid_user.posts.first().author == valid_user
