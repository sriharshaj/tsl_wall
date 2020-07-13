from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from wall.serializers import PostSerializer, UserSerializer, UserSerializerWithToken
from wall.models import Post
from wall.emails import send_user_welcome_email


class IsAuthenticatedForGetOnly(BasePermission):
    """
    Request is authenticated if user logged in, or is GET.
    """

    def has_permission(self, request, view):
        if (request.method in ['GET'] or request.user.is_authenticated):
            return True
        return False


class PostView(ListCreateAPIView):
    """
    Create a new post and lists all posts
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedForGetOnly]

    def perform_create(self, serializer):
        serializer.save(author_id=self.request.user.id)


@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """

    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserView(CreateAPIView):
    """
    Create a new user. 
    """
    serializer_class = UserSerializerWithToken
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        instance = serializer.save()
        send_user_welcome_email(instance.email)
