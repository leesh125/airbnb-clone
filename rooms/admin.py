from django.contrib import admin
from django.utils.html import mark_safe
from . import models


# admin 패널에서 RoomType을 추가하기 위해 작성
@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = ("name", "used_by")

    # ameni,facit 등등 몇개를 가지고 있는지 알기위해
    def used_by(self, obj):
        return obj.rooms.count()

    pass


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    fieldsets = (
        (
            "Basic Info",  # 전체 필드카테고리 (파란색)
            {"fields": ("name", "description", "country", "address", "price")},  # 필드들
        ),
        (
            "Times",
            {"fields": ("check_in", "check_out", "instant_book")},
        ),
        (
            "Spaces",
            {
                "fields": (
                    "guests",
                    "beds",
                    "bedrooms",
                    "baths",
                )
            },
        ),
        (
            "More About the Space",
            {
                "classes": ("collapse",),  # 필드 내용이 많으면 접을 수 있음
                "fields": (
                    "amenities",
                    "facilities",
                    "house_rules",
                ),
            },
        ),
        (
            "Last Detail",
            {"fields": ("host",)},
        ),
    )

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
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    # admin 패널에서 해당 필드 기준으로 정렬할 수 있음
    ordering = ("name", "price", "bedrooms")

    list_filter = (
        "instant_book",
        "host__superhost",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    # admin 패널에서 설정한 필드를 검색할 수 있음(와래키의 필드 접근은 __ 로 구분)
    search_fields = (
        "city",
        "^host__username",  # ^ : 시작하는 단어가 같아야함
    )

    # ManyToMany를 깔끔하게 정리하기 위해
    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )

    # amenity 등등 의 갯수를 세는 custom admin 사용자 정의 함수
    def count_amenities(self, obj):  # self는 현재 클래스, object는 현재 행
        # 현재 room 객체가 가지고 있는 amenity의 갯수를 return
        return obj.amenities.count()

    # admin 패널에 사용자 정의 컬럼 이름설정
    # count_amenities.short_description = "hello sexy!"

    def count_photos(self, obj):
        return obj.photos.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):  # obj: Photo model 객체
        # 현재 행의 photo객체의 파일 url을 얻은 후 img태그로 출력(보안 기능으로 막혀있지만 mark_safe로 html 태그 작성 가능)
        return mark_safe(f'<img width="50px" src="{obj.file.url}" />')

    get_thumbnail.short_decription = "Thumbnail"