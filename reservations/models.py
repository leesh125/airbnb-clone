import datetime
from django.db import models
from django.utils import timezone  # python 라이브러리 사용하지 않는이유(애플리케이션 서버의 시간을 알기위해)
from core import models as core_models
from . import managers

# check_in과 check_out 사이의 날짜를 확인하기 위한 클래스
class BookedDay(core_models.TimeStampedModel):

    day = models.DateField()
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Booked Day"
        verbose_name_plural = "Booked Days"

    def __str__(self):
        return str(self.day)


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
    objects = managers.CustomReviewManager()

    def __str__(self):
        return f"{self.room} - {self.check_in}"

    # 현재 해당 room에 묶는 사람이 있는지
    def in_progress(self):
        now = timezone.now().date()
        return now >= self.check_in and now <= self.check_out

    in_progress.boolean = True  # admin 패널에 boolean을 아이콘으로 표시하려고

    def is_finished(self):
        now = timezone.now().date()
        return now > self.check_out

    is_finished.boolean = True

    def save(self, *args, **kwargs):
        if self.pk is None:  # 새로 생성된 예약인지 확인
            start = self.check_in
            end = self.check_out
            difference = end - start
            existing_booked_day = BookedDay.objects.filter(
                day__range=(start, end)
            ).exists()  # 시작과 끝일 사이에 예약된 날이 있는지 확인
            if not existing_booked_day:
                super().save(*args, **kwargs)
                for i in range(difference.days + 1):
                    day = start + datetime.timedelta(days=i)
                    BookedDay.objects.create(day=day, reservation=self)
                return
        else:
            return super().save(*args, **kwargs)


# 현재 시간 갖고오는 함수
def get_now_date():
    return timezone.now().date()