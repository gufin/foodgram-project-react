from rest_framework import permissions, status, views
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from .serializers import CustomAuthTokenSerializer


class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {'auth_token': token.key},
            status=status.HTTP_201_CREATED
        )


class DestroyTokenAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        if not user:
            Response(
                {'detail': 'Authentication credentials were not provided.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            Response(
                {'detail': 'Token does not exist.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
