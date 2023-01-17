from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

# Create your views here.

class UserExistsView(APIView):

    """
    Endpoint used by the user-interaction-service to check if the user exists.
    """    

    def get(self, request,id):

        try:
            user = User.objects.get(pk=id)
            return Response({"data":"User Exists!"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"data":"User Doesn't exists!"},status=status.HTTP_400_BAD_REQUEST)


class UserListCreateView(ListCreateAPIView):

    """
    Endpoint to Get all the user as well as create a user by using methods GET, POST respectively
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRetrieveUpdateDes(RetrieveUpdateDestroyAPIView):

    """
    Endpoint to retrieve, update and destroy a single User by using methods GET, PUT, DELETE respectively.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer