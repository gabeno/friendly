from api.models import Post, User
from api.serializers import PostSerializer, UserSerializer
from api.utils import remote_address
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from friendly.tasks import set_user_metadata


class UserCreateView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            ip = remote_address(request)
            set_user_metadata.delay(serializer.data["id"], ip)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    permission_classes = (IsAuthenticated,)

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
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = PostSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    permission_classes = (IsAuthenticated,)

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
    permission_classes = (IsAuthenticated,)

    def _get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        post = self._get_object(pk)
        user = request.user
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
        else:
            post.likes.add(user)
        serializer = PostSerializer(post, context={"request": request})
        return Response(serializer.data)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            token = RefreshToken(request.data.get("refresh"))
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
