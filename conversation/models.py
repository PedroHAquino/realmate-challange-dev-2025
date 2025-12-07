import uuid
from django.db import models
from .enums import ConversationState, MessageDirection


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    state = models.CharField(max_length=10, choices=ConversationState.choices, default=ConversationState.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)

    def close(self):
        self.state = ConversationState.CLOSED
        self.save()

    class Meta:
        db_table = "conversation"


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, related_name="messages", on_delete=models.CASCADE)
    direction = models.CharField(max_length=10, choices=MessageDirection.choices)
    content = models.TextField()
    timestamp = models.DateTimeField()

    class Meta:
        db_table = "message"
        ordering = ["timestamp"]
