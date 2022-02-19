from django.contrib import admin
from . import models


class ProgressListFilter(admin.SimpleListFilter):
    title = "In Progress"  # 필터에 By .... 에 들어갈 녀석을 적음
    parameter_name = "in_progress"  # 필터링할 녀석

    # lookups 멤버함수는 장고 프레임워크가 찾아서(look up) 필터링할 값에 대한 정보를 넣어주는 역할을 함
    def lookups(self, request, model_admin):
        return (
            ("True", "True"),  # 첫 번째 인자는 필터링할 실제 값, 두 번째 인자는 필터에 보여질 값
            ("False", "False"),
        )

    def queryset(self, request, queryset):
        now = models.get_now_date()

        if self.value() == "True":
            # check_in__?? 의 의미는 check_in이라는 컬럼을 기준으로 어떻게 필터링할 건지를 제시.
            return queryset.filter(check_in__lt=now, check_out__gt=now)

        elif self.value() == "False":
            return queryset.exclude(check_in__lt=now, check_out__gt=now)


class FinishedListFilter(admin.SimpleListFilter):
    title = "Is Finished"
    parameter_name = "is_finished"

    def lookups(self, request, model_admin):
        return (
            ("True", "True"),
            ("False", "False"),
        )

    def queryset(self, request, queryset):
        now = models.get_now_date()

        if self.value() == "True":
            return queryset.filter(check_out__lt=now)

        elif self.value() == "False":
            return queryset.exclude(check_out__lt=now)


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):

    """ Reservation Admin Definition """

    list_display = (
        "room",
        "status",
        "check_in",
        "check_out",
        "guest",
        "in_progress",
        "is_finished",
    )

    list_filter = ("status", ProgressListFilter, FinishedListFilter)


@admin.register(models.BookedDay)
class BookedDayAdmin(admin.ModelAdmin):

    list_display = ("day", "reservation")
