from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from rooms import models as room_models
from . import models


# User Admin 안에 Room admin 추가
class RoomInline(admin.TabularInline):

    model = room_models.Room


@admin.register(models.User)  # admin.site.register(models.User, CustomUserAdmin) 와 동일
class CustomUserAdmin(UserAdmin):

    """ Custom User Admin """

    inlines = (RoomInline,)

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",  # 필드셋(admin패널 파란색 필드)의 이름
            {
                "fields": (  # 필드 지정
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                )
            },
        ),
    )

    list_filter = UserAdmin.list_filter + ("superhost",)

    # admin 패널에서 보일 필드
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
    )

    ### UserAdmin으로 대체 가능
    # # admin 패널에 list_display로 생성된 필드(컬럼)의 값을 볼 수 있다.
    # list_display = ("username", "email", "gender", "language", "currency", "superhost")
    # # admin 패널에 list_filter로 지정한 필드로 필터링 할 수 있다.
    # list_filter = (
    #     "language",
    #     "currency",
    #     "superhost",
    # )
