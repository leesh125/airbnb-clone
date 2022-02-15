# * import 관례
# 0. 파이썬 관련한 것 (ex.import os)
# 1. django와 관련된 것들
# 2. 외부 패키지
# 3. 내가 만든 패키지
from django.db import models
from django.urls import reverse  # 지정한 url name을 return 하기위해
from django_countries.fields import CountryField
from core import models as core_models


class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """ RoomType Model Definition """

    class Meta:
        verbose_name = "Room Type"
        # ordering = ["created"] # 객체들의 정렬 순서를 정할 수 있음


class Amenity(AbstractItem):

    """ Amenity Model Definition """

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):

    """ Facilty Model Definition """

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):

    """ HouseRule Model Definition """

    class Meta:
        verbose_name = "House Rule"


# room의 사진을 위한 클래스
class Photo(core_models.TimeStampedModel):

    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField(
        upload_to="room_photos"
    )  # uploads 폴더안에 어떤 폴더에다가 photo를 업로드 할 것인지
    # Room은 사진을 여러개, 한 사진은 하나의 Room에 해당
    # Room 클래스(객체)를 String으로도 받을 수 있음
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """ Room Model Definition """

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField(help_text="How many people will be staying?")
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    # user model을 외래키로 연결(다대일)
    # related_name: 외래키로 연결된 User가 Room을 찾기위한 방법(room_set의 이름 변경)
    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )
    # RoomType을 다대다로
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    # Room 객체를 문자열로 어떻게 보이게 할 것인지.
    def __str__(self):
        return self.name

    # admin, view 모든 곳에서 save시에 수행됨
    def save(self, *args, **kwargs):
        self.city = self.city.title()  # city의 단어 앞글자만 대문자로
        super().save(*args, **kwargs)  # 진짜 save(저장) method 호출

    # admon 패널에 해당 room 객체가 어떻게 화면에 보이는지
    def get_absolute_url(self):
        # urlname으로 지정한 곳으로 이동(kwargs: 매개변수 포함)
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def total_rating(self):
        # review 모델에 있는 room(foreign key로 연결) 필드에서 reviews를 읽어옴
        all_reviews = self.reviews.all()
        try:
            all_ratings = 0
            for review in all_reviews:
                all_ratings += review.rating_average()
            return round(all_ratings / len(all_reviews), 2)
        except ZeroDivisionError:  # 리뷰가 하나도 없을때의 예외처리
            return 0

    # 첫번째 사진 가져오는 함수
    def first_photo(self):
        # 열거식(,)으로 배열에 첫번째 값 빼오기
        (photo,) = self.photos.all()[:1]
        return photo.file.url

    def get_next_four_photos(self):
        photos = self.photos.all()[1:5]
        return photos
