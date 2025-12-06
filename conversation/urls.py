from django.urls import path
from .views import ConversationDetailView, WebhookView

urlpatterns = [
    path("webhook/", WebhookView.as_view()),
    path("conversation/<uuid:pk>/", ConversationDetailView.as_view()),
]
