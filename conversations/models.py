from tkinter import CASCADE
from django.db import models
from core import models as core_models


class Conversation(core_models.TimeStampedModel):

    """ Conversation Model Definition """

    participants = models.ManyToManyField("users.User", blank=True)

    def __str__(self):
        return str(self.created)  # dateField여서 객체가 보이러면 str으로 해야함


class Message(core_models.TimeStampedModel):

    """ Message Model Definition """

    message = models.TextField()
    user = models.ForeignKey("users.User", on_delete=CASCADE)
    conversation = models.ForeignKey("Conversation", on_delete=CASCADE)

    def __str__(self):
        return f"{self.user} says: {self.message}"
