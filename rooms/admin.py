from django.contrib import admin
from . import models


# admin 패널에서 RoomType을 추가하기 위해 작성
@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    pass


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
    )

    list_filter = ("instant_book", "city", "country")

    # admin 패널에서 설정한 필드를 검색할 수 있음(와래키의 필드 접근은 __ 로 구분)
    search_fields = (
        "city",
        "^host__username",  # ^ : 시작하는 단어가 같아야함
    )


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ """

    pass