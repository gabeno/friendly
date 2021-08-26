import pytest
from api.models import Post
from django.db.utils import IntegrityError
from django.utils import timezone


@pytest.mark.django_db
class TestPostModel(object):
    def test_post_create_details_ok(self):
        NOW = timezone.now()
        content = """Once upon a tyne, there lived a great old fellow who had
an amazing ability to see yonder!

He led a simple life back at the village. He was quite a honorable
person and very respected amongst his peers.

Abrupt end of story!!"""

        post = Post.objects.create(
            title="Cést la vie 😶",
            content=content,
            created_when=NOW,
        )

        assert post.title == "Cést la vie 😶"
        assert post.content == content
        assert post.created_when == NOW
        assert post.likes_count == 0
        assert post.author_id == 99

    def test_create_one_post_count_ok(self):
        before_count = Post.objects.count()
        Post.objects.create(
            title="title",
            content="content",
        )

        assert Post.objects.count() == before_count + 1

    def test_post_update_title_ok(self):
        title = "title"
        new_title = "new title"
        p = Post.objects.create(
            title=title,
            content="content",
        )
        p.title = new_title
        p.save()

        assert p.title != title
        assert p.title == new_title

    def test_post_add_like_increases_count(self):
        p = Post.objects.create(
            title="title",
            content="content",
        )
        likes_count_before = p.likes_count
        p.likes_count += 1
        p.save()

        assert p.likes_count == likes_count_before + 1

    def test_create_multiple_posts_count_ok(self):
        before_count = Post.objects.count()
        Post.objects.create(
            title="title 1",
            content="content 1",
        )
        Post.objects.create(
            title="title 2",
            content="content 2",
        )

        assert Post.objects.count() == before_count + 2

    def test_delete_post_ok(self):
        p = Post.objects.create(
            title="title",
            content="content",
        )
        before_count = Post.objects.count()
        p.delete()

        assert Post.objects.count() == before_count - 1

    def test_create_post_with_unique_title(self):
        with pytest.raises(IntegrityError):
            Post.objects.create(title="title")
            Post.objects.create(title="title")
