from tkinter import CASCADE
from django.db import models
from core import models as core_models


class Review(core_models.TimeStampedModel):

    """ Review Model definition """

    review = models.TextField()
    accuracy = models.IntegerField()
    communication = models.IntegerField()
    cleanliness = models.IntegerField()
    location = models.IntegerField()
    check_in = models.IntegerField()
    value = models.IntegerField()
    user = models.ForeignKey("users.User", on_delete=CASCADE)
    room = models.ForeignKey("rooms.Room", on_delete=CASCADE)

    def __str__(self):
        # Review 객체를 admin 패널에서 "review - Room(객실이름)" 이렇게 표시 가능함
        return f"{self.review} - {self.room}"
