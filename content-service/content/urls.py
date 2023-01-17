from django.urls import path
from .views import UploadFileView, NewContentView, TopContentView, ContentCreateView,ContentRetrieveUpdateDes

urlpatterns = [
    path('',ContentCreateView.as_view()),
    path('<int:pk>', ContentRetrieveUpdateDes.as_view()),
    path('ingest_data/',UploadFileView.as_view()),
    path('new-content/',NewContentView.as_view()),
    path('top-content/',TopContentView.as_view()),
]