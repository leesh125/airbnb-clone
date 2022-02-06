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
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reviews", on_delete=models.CASCADE
    )

    def __str__(self):
        # Review 객체를 admin 패널에서 "review - Room(객실이름)" 이렇게 표시 가능함
        return f"{self.review} - {self.room}"

    # admin과 프론트엔트에서 보이기 위해 model에 작성
    def rating_average(self):
        avg = (
            self.accuracy
            + self.communication
            + self.cleanliness
            + self.location
            + self.check_in
            + self.value
        ) / 6
        return round(avg, 2)  # 두자리 수 까지 반올림

    rating_average.short_description = "Avg"