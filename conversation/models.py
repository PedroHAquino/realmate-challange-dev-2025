import uuid
from django.db import models
from .enums import ConversationState, MessageDirection


class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=10, choices=ConversationState.choices, default=ConversationState.OPEN)

    def close(self):
        self.state = ConversationState.CLOSED
        self.save()


class Message(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        ordering = ["timestamp"]