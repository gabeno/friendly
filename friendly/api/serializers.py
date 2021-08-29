from api.models import Post, User
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    author = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="user-detail"
    )

    class Meta:
        model = Post
        fields = ["id", "content", "author", "created_when", "likes_count"]


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.HyperlinkedRelatedField(
        read_only=True, many=True, view_name="post-detail", required=False
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "created_when",
            "geo_data",
            "posts",
        ]

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user
