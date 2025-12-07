from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from .models import Conversation
from .serializers import ConversationSerializer
from .services.webhook_handler import WebhookHandler

class ConversationDetailView(RetrieveAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

class WebhookView(APIView):
    http_method_names = ["post"]

    def post(self, request):
        return WebhookHandler.process(request.data)
