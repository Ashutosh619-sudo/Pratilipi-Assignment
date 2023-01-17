from django.urls import path, include
from .views import UserExistsView, UserListCreateView, UserRetrieveUpdateDes
from rest_framework.authtoken import views


urlpatterns = [
    path('', UserListCreateView.as_view()),
    path('<int:pk>', UserRetrieveUpdateDes.as_view()),
    path('auth_token/',views.obtain_auth_token),
    path('exists/<int:id>', UserExistsView.as_view()),
    
]