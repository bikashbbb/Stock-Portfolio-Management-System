from statistics import mode
from user_profile.models import UserProfile
from rest_framework import viewsets, permissions, generics, mixins
from .serializers import UserProfileSerializer
from rest_framework.response import Response
from rest_framework import status
# UserProfile Viewset for get user profile and create user profile

class UserProfileViewSet(viewsets.ModelViewSet):
    # validate if the user login
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        # get the user profile information of the login user

        if getattr(self, 'swagger_fake_view', False):
            return UserProfile.objects.none() 
        else:
            return self.request.user.user_profile.all()

    def perform_create(self, serializer):
        # save the created user information with the owner id equivalent to the auth user id
        serializer.save(owner=self.request.user)

class UserProfileUpdateViewSet(viewsets.ModelViewSet, generics.UpdateAPIView, mixins.UpdateModelMixin   ):
    # validate if the user login
    model= UserProfile
    queryset = UserProfile.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = UserProfileSerializer
        
    
    def get_object(self):
        return self.request.user.user_profile.all()

    def update(self, request, *args, **kwargs):
        # get the instance which owner_id equivalent to the auth user id
        instance = self.get_object().get(owner_id=self.request.user)
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        # update the user profile information
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
