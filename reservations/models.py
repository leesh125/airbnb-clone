from django.db import models
from django.utils import timezone  # python 라이브러리 사용하지 않는이유(애플리케이션 서버의 시간을 알기위해)
from core import models as core_models


class Reservation(core_models.TimeStampedModel):

    """ Reservation Model Definition """

    STATUS_PENDING = "Pending"
    STATUS_CONFIRMED = "Confirmed"
    STATUS_CANCELED = "Canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Pending"),
        (STATUS_CANCELED, "Pending"),
    )

    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey(
        "users.User", related_name="reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reservations", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.room} - {self.check_in}"

    # 현재 해당 room에 묶는 사람이 있는지
    def in_progress(self):
        now = timezone.now().date()
        return now > self.check_in and now < self.check_out

    in_progress.boolean = True  # admin 패널에 boolean을 아이콘으로 표시하려고

    def is_finished(self):
        now = timezone.now().date()
        return now > self.check_out

    is_finished.boolean = True