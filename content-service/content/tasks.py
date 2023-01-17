from celery import shared_task
import io, csv, pandas as pd
from .models import Content
from django.core.files.storage import FileSystemStorage
from pathlib import Path
import json


@shared_task
def ingest_data_csv(path,file_name):

    storage = FileSystemStorage()
    path_object = Path(path)
    print(path_object)
    with open(path,'r') as file:

        reader = csv.reader(file)
        next(reader)

        for id_, row in enumerate(reader):
            (
                title,
                story,
                date_published,
                user_id
            ) = row

            new_file = Content(
                title = title,
                story = story,
                date_published = date_published,
                user_id = user_id
            )
            new_file.save()
    
    storage.delete(path)


@shared_task
def like_event(content_id):

    
    content = Content.objects.get(pk=content_id)

    content.likes += 1

    content.save()