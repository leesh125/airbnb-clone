from tkinter import CASCADE
from django.db import models
from core import models as core_models


class Conversation(core_models.TimeStampedModel):

    """ Conversation Model Definition """

    participants = models.ManyToManyField(
        "users.User", related_name="conversation", blank=True
    )

    def __str__(self):
        usernames = []
        for user in self.participants.all():
            usernames.append(user.username)

        return ", ".join(usernames)  # 대화 참여자들을 문자열로 반환

    def count_messages(self):
        # Conversation 클래스는 messages가 없다
        # 하지만 Message는 Conversation과 외래키로 연결되어있다.
        return self.messages.count()

    count_messages.short_description = "Number of Messages"

    def count_participants(self):
        return self.participants.count()

    count_participants.short_description = "Number of Participants"


class Message(core_models.TimeStampedModel):

    """ Message Model Definition """

    message = models.TextField()
    user = models.ForeignKey(
        "users.User", related_name="messages", on_delete=models.CASCADE
    )
    conversation = models.ForeignKey(
        "Conversation", related_name="messages", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} says: {self.message}"
