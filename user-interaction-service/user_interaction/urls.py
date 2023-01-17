from django.urls import path
from .views import InteractionView, TopInteractionsView

urlpatterns = [
    path('interact/', InteractionView.as_view()),
    path('top-interactions/',TopInteractionsView.as_view())
]
