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
            "password",
            "created_on_holiday",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        instance = self.Meta.model(**validated_data)
        instance.set_password(password)
        instance.save()
        return instance
