from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import InteractionSerializer
import requests
from rest_framework.views import Response
from rest_framework import status
from .services import send_like_event

from .models import Interaction
from django.db.models import Count

from django.db.models import Q
# Create your views here.


class InteractionView(APIView):

    """
    Endpoint to add interaction of user i.e like interaction if user likes a content and read interaction if user reads a content.
    It first verifies if the user exists by calling the user-service's exists endpoint then adds the particular interaction to the database,
    If the interaction type is like then it produces a like_event in rabbitmq that is picked by the consumer running in the content service 
    that increases the like of that content.
    """

    def post(self, request):

        response = requests.get(f'http://user-service:8002/users/exists/{request.data["user_id"]}')
        if response.status_code != 200:
            return Response({"data":"User Doesn't exists!"},status=status.HTTP_400_BAD_REQUEST)

        
        serializer = InteractionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)   
        serializer.save()

        if request.data["interaction_type"] == "like":
            send_like_event(request.data["content_id"])
        

        return Response({"data":"Successfully added the interaction"},status=status.HTTP_201_CREATED)


class TopInteractionsView(APIView):

    """
    This is an internal API used by the content-service to that the top interactions in terms of number of likes and read.
    The content-service then uses this information to show the top content.
    """

    def get(self, request):

        interactions = Interaction.objects.filter(interaction_type__in=['like','read']).annotate(like_count=Count('interaction_type',filter=Q(interaction_type='like')),read_count=Count('interaction_type',filter=Q(interaction_type='read'))).order_by('like_count', 'read_count')
        serializer = InteractionSerializer(interactions,many=True)

        return Response(serializer.data)


