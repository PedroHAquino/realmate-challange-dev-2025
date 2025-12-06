from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_datetime
from .models import Conversation, Message
from .enums import ConversationState, MessageDirection
from rest_framework.generics import RetrieveAPIView
from .models import Conversation
from .serializers import ConversationSerializer
import traceback

class ConversationDetailView(RetrieveAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

class WebhookView(APIView):
    http_method_names = ["post"]

    def get(self, request, *args, **kwargs):
        return Response({"detail": "Method GET not allowed"}, status=405)

    def head(self, request, *args, **kwargs):
        return Response(status=405)

    def options(self, request, *args, **kwargs):
        return Response(status=405)

    def post(self, request):
        try:
            event_type = request.data.get("type")
            data = request.data.get("data", {})
            timestamp = request.data.get("timestamp")

            if event_type == "NEW_CONVERSATION":
                return self.handle_new_conversation(data)

            elif event_type == "NEW_MESSAGE":
                return self.handle_new_message(data, timestamp)

            elif event_type == "CLOSE_CONVERSATION":
                return self.handle_close_conversation(data)

            return Response({"error": "Invalid event type"}, status=400)

        except Exception as e:
            return Response({"error": str(e)}, status=400)

    def handle_new_conversation(self, data):
        conv_id = data.get("id")

        if Conversation.objects.filter(id=conv_id).exists():
            return Response({"detail": "Conversation already exists"}, status=200)

        Conversation.objects.create(
            id=conv_id,
            state=ConversationState.OPEN,
        )
        return Response({"detail": "Conversation created"}, status=201)

    def handle_new_message(self, data, timestamp):
        conv_id = data.get("conversation_id")
        msg_id = data.get("id")

        try:
            conv = Conversation.objects.get(id=conv_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found"}, status=400)

        if conv.state == ConversationState.CLOSED:
            return Response({"error": "Conversation is closed"}, status=400)

        if Message.objects.filter(id=msg_id).exists():
            return Response({"detail": "Message already exists"}, status=200)

        Message.objects.create(
            id=msg_id,
            conversation=conv,
            direction=data.get("direction"),
            content=data.get("content"),
            timestamp=parse_datetime(timestamp),
        )

        return Response({"detail": "Message created"}, status=201)

    def handle_close_conversation(self, data):
        conv_id = data.get("id")

        try:
            conv = Conversation.objects.get(id=conv_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found"}, status=400)

        conv.state = ConversationState.CLOSED
        conv.save()

        return Response({"detail": "Conversation closed"}, status=200)
