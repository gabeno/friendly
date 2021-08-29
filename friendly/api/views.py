from api.models import Post, User
from api.serializers import PostSerializer, UserSerializer
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class UserCreateView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # XXX defer holiday and geo_data fetch
            return Response(
                serializer.validated_data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    def _get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self._get_object(pk)
        serializer = UserSerializer(user, context={"request": request})
        return Response(serializer.data)


class PostCreateView(APIView):
    def post(self, request):
        serializer = PostSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            author = User.objects.get(pk=request.data.get("id"))  # XXX
            serializer.save(author=author)  # XXX
            # serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    def _get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self._get_object(pk)
        serializer = PostSerializer(user, context={"request": request})
        return Response(serializer.data)


class LikesView(APIView):
    def _get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        post = self._get_object(pk)
        data = {"likes_count": int(request.data.get("likes_count")) + 1}
        serializer = PostSerializer(post, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
