from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from .models import Content
from .tasks import ingest_data_csv
from rest_framework import status

from .serializers import ContentSerializer

from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage

import requests

# Create your views here.

class UploadFileView(APIView):
    """
    Endpoint to upload custom content data. The data must be a csv file, 
    it must only contain three column user_id, title, story, date_published.
    The data must be provided in file attribute in the request.
    """

    def post(self,request):
        # used to store temporary file in tmp folder
        fs = FileSystemStorage(location='tmp/')

        file = request.FILES["file"]
        if file.name.split(".")[-1] != "csv":
            return Response({"data":"Only CSV file is allowed!"}, status=status.HTTP_400_BAD_REQUEST)

        content = file.read()

        file_content = ContentFile(content)
        file_name = fs.save("tmp.csv",file_content)


        ingest_data_csv.delay(fs.path(file_name),file.name
        )

        return Response({"data":"CSV successfully uploaded!"},status=status.HTTP_201_CREATED)


class NewContentView(APIView):

    """
        Endpoint to get new content, its sorted by the date_published.
    """

    def get(self,request):

        contents = Content.objects.all().order_by('-date_published')
        serializer = ContentSerializer(contents,many=True)

        return Response({"data":serializer.data},status=status.HTTP_200_OK)


class TopContentView(APIView):

    """
    Endpoint to get the top content by like and read, 
    this view calls the user-interaction-service's top-interaction endpoint to get the most liked and read content.
    """

    def get(self, request):

        response = requests.get(f"http://user-interaction-service:8001/user-interaction/top-interactions/")
        interaction_data = response.json()

        content_ids = set()
        for data in interaction_data:
            content_ids.add(data["content_id"])
        

        contents = Content.objects.filter(id__in=list(content_ids))
        serializer = ContentSerializer(contents, many=True)

        return Response({"data":serializer.data})

class ContentCreateView(ListCreateAPIView):

    """
    Endpoint to create a content from the api.
    """

    queryset = Content.objects.all()
    serializer_class = ContentSerializer


class ContentRetrieveUpdateDes(RetrieveUpdateDestroyAPIView):

    """
    Endpoint to retrieve, update and destroy a single content by using the methods GET, PUT, DELETE respectively.
    """

    queryset = Content.objects.all()
    serializer_class = ContentSerializer