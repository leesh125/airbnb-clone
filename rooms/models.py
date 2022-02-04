# * import 관례
# 0. 파이썬 관련한 것 (ex.import os)
# 1. django와 관련된 것들
# 2. 외부 패키지
# 3. 내가 만든 패키지
from django.db import models
from django_countries.fields import CountryField
from core import models as core_models
from users import models as user_models


class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    pass


class Room(core_models.TimeStampedModel):

    """ Room Model Definition """

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    # user model을 외래키로 연결(다대일)
    host = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    # RoomType을 다대다로
    room_type = models.ManyToManyField(RoomType, blank=True)

    # Room 객체를 문자열로 어떻게 보이게 할 것인지.
    def __str__(self):
        return self.name