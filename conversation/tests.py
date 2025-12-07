import pytest
import uuid
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone

from conversation.models import Conversation, Message
from conversation.enums import ConversationState
from conversation.services.webhook_handler import WebhookHandler
import uuid
from unittest.mock import patch, MagicMock
from django.utils import timezone
from rest_framework.response import Response

from conversation.enums import ConversationState
from conversation.services.webhook_handler import WebhookHandler


class TestWebhookHandlerProcess:

    def test_invalid_event_type(self):
        payload = {"type": "INVALID"}
        response = WebhookHandler.process(payload)
        assert response.status_code == 400
        assert response.data["error"] == "Invalid event type"


class TestNewConversation:

    @patch("conversation.services.webhook_handler.Conversation")
    def test_create_new_conversation(self, MockConversation):
        conv_id = str(uuid.uuid4())

        MockConversation.objects.filter.return_value.exists.return_value = False

        payload = {
            "type": "NEW_CONVERSATION",
            "data": {"id": conv_id}
        }

        response = WebhookHandler.process(payload)

        MockConversation.objects.create.assert_called_once_with(
            id=conv_id,
            state=ConversationState.OPEN,
        )

        assert response.status_code == 201

    @patch("conversation.services.webhook_handler.Conversation")
    def test_conversation_already_exists(self, MockConversation):
        conv_id = str(uuid.uuid4())

        MockConversation.objects.filter.return_value.exists.return_value = True

        payload = {
            "type": "NEW_CONVERSATION",
            "data": {"id": conv_id}
        }

        response = WebhookHandler.process(payload)

        assert response.status_code == 200
        assert response.data["detail"] == "Conversation already exists"


class TestNewMessage:

    @patch("conversation.services.webhook_handler.Message")
    @patch("conversation.services.webhook_handler.Conversation")
    def test_message_created(self, MockConversation, MockMessage):
        conv_id = str(uuid.uuid4())
        msg_id = str(uuid.uuid4())

        mock_conv = MagicMock(state=ConversationState.OPEN)
        MockConversation.objects.get.return_value = mock_conv
        MockMessage.objects.filter.return_value.exists.return_value = False

        payload = {
            "type": "NEW_MESSAGE",
            "data": {
                "id": msg_id,
                "conversation_id": conv_id,
                "direction": "RECEIVED",
                "content": "Olá"
            },
            "timestamp": timezone.now().isoformat(),
        }

        response = WebhookHandler.process(payload)

        MockMessage.objects.create.assert_called_once()
        assert response.status_code == 201

    @patch("conversation.services.webhook_handler.Conversation")
    def test_message_conversation_not_found(self, MockConversation):
        MockConversation.DoesNotExist = type("DoesNotExist", (Exception,), {})
        MockConversation.objects.get.side_effect = MockConversation.DoesNotExist()

        msg_id = str(uuid.uuid4())
        conv_id = str(uuid.uuid4())

        payload = {
            "type": "NEW_MESSAGE",
            "data": {"id": msg_id, "conversation_id": conv_id},
            "timestamp": timezone.now().isoformat(),
        }

        response = WebhookHandler.process(payload)

        assert response.status_code == 400
        assert response.data["error"] == "Conversation not found"


    @patch("conversation.services.webhook_handler.Message")
    @patch("conversation.services.webhook_handler.Conversation")
    def test_message_already_exists(self, MockConversation, MockMessage):
        conv = MagicMock(state=ConversationState.OPEN)
        MockConversation.objects.get.return_value = conv

        MockMessage.objects.filter.return_value.exists.return_value = True

        payload = {
            "type": "NEW_MESSAGE",
            "data": {"id": "msg", "conversation_id": "whatever"},
            "timestamp": timezone.now().isoformat(),
        }

        response = WebhookHandler.process(payload)
        assert response.status_code == 200
        assert response.data["detail"] == "Message already exists"

    @patch("conversation.services.webhook_handler.Conversation")
    def test_message_on_closed_conversation(self, MockConversation):
        conv = MagicMock(state=ConversationState.CLOSED)
        MockConversation.objects.get.return_value = conv

        payload = {
            "type": "NEW_MESSAGE",
            "data": {"id": "msg", "conversation_id": "id"},
            "timestamp": timezone.now().isoformat(),
        }

        response = WebhookHandler.process(payload)
        assert response.status_code == 400
        assert response.data["error"] == "Conversation is closed"


class TestCloseConversation:

    @patch("conversation.services.webhook_handler.Conversation")
    def test_close_conversation_not_found(self, MockConversation):
        class FakeDoesNotExist(Exception):
            pass

        MockConversation.DoesNotExist = FakeDoesNotExist
        MockConversation.objects.get.side_effect = FakeDoesNotExist()

        payload = {
            "type": "CLOSE_CONVERSATION",
            "data": {"id": str(uuid.uuid4())},
        }

        response = WebhookHandler.process(payload)

        assert response.status_code == 400
        assert response.data["error"] == "Conversation not found"