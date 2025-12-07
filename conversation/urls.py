from django.urls import path
from .views import ConversationDetailView, WebhookView, ConversationListView

urlpatterns = [
    path("webhook/", WebhookView.as_view()),
    path("conversations/", ConversationListView.as_view()),
    path("conversation/<uuid:pk>/", ConversationDetailView.as_view()),
]
