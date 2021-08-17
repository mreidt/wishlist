from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt import authentication
from user.serializers import SuperuserSerializer, UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateSuperuserView(generics.CreateAPIView):
    """Create a new superuser in the system"""
    serializer_class = SuperuserSerializer
    authentication_classes = (authentication.JWTAuthentication,)
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    )


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authentication user"""
        return self.request.user

    def get_queryset(self):
        """Get data about authenticated user"""
        return get_user_model().objects.get(id=self.request.user.id)


class RemoveUserView(generics.DestroyAPIView):
    """Remove users from the system"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def remove_user(self, user):
        """Removes an user object"""
        user.delete()

    def delete(self, request, *args, **kwargs):
        """Removes an user object"""
        remove_id = request.data.get('user_id', None)
        if remove_id:
            remove_id = int(remove_id)
            if self.request.user.id == remove_id:
                self.remove_user(self.request.user)
                return Response(status=status.HTTP_204_NO_CONTENT)
            if self.request.user.is_superuser:
                self.remove_user(get_user_model().objects.get(pk=remove_id))
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            self.remove_user(self.request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)


class ListUsersView(generics.ListAPIView):
    """List users from the system"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.JWTAuthentication,)
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    )
    queryset = get_user_model().objects.all()
