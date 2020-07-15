from wall.serializers import UserSerializer


def my_jwt_response_handler(token, user=None, request=None):
    user = UserSerializer(user, context={'request': request}).data
    return dict({'token': token}, **user)
