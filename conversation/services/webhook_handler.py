from django.utils.dateparse import parse_datetime
from rest_framework.response import Response
from rest_framework import status

from conversation.models import Conversation, Message
from conversation.enums import ConversationState


class WebhookHandler:

    @staticmethod
    def process(payload):
        event_type = payload.get("type")
        data = payload.get("data", {})
        timestamp = payload.get("timestamp")

        if event_type == "NEW_CONVERSATION":
            return WebhookHandler.handle_new_conversation(data)

        elif event_type == "NEW_MESSAGE":
            return WebhookHandler.handle_new_message(data, timestamp)

        elif event_type == "CLOSE_CONVERSATION":
            return WebhookHandler.handle_close_conversation(data)

        return Response({"error": "Invalid event type"}, status=400)

    @staticmethod
    def handle_new_conversation(data):
        conv_id = data.get("id")

        if Conversation.objects.filter(id=conv_id).exists():
            return Response({"detail": "Conversation already exists"}, status=200)

        Conversation.objects.create(
            id=conv_id,
            state=ConversationState.OPEN,
        )
        return Response({"detail": "Conversation created"}, status=201)

    @staticmethod
    def handle_new_message(data, timestamp):
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

    @staticmethod
    def handle_close_conversation(data):
        conv_id = data.get("id")

        try:
            conv = Conversation.objects.get(id=conv_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found"}, status=400)

        conv.state = ConversationState.CLOSED
        conv.save()

        return Response({"detail": "Conversation closed"}, status=200)
