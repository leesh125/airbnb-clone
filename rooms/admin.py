from django.contrib import admin
from . import models


# admin 패널에서 RoomType을 추가하기 위해 작성
@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    pass


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    pass