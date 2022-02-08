from math import ceil
from django.shortcuts import render  # HttpResponse안에 html을 넣어서 보내줄 수 있다.
from django.http import HttpResponse
from . import models


# 장고는 Httprequest를 파이썬 객체로 변환해 준다.
def all_rooms(request):
    # request.Get : GET 메소드로 보내지는 요청 파라미터를 불러옴
    page = int(request.GET.get("page", 1))  # 파라미터 값을 가져옴(기본값 0)
    page = int(page or 1)  # 잘못된 파라미터가 올 경우 1로 대체
    page_size = 10  # 보여질 room의 수
    limit = page_size * page  # 해당 페이지에서 보여질 room의 마지막 수
    offset = limit - page_size  # 해당 페이지에서 보여질 room의 첫번째 수
    page_count = ceil(
        models.Room.objects.count() / page_size
    )  # 전체 페이지수(실수여서 올림해서 보내야함)
    all_rooms = models.Room.objects.all()[offset:limit]
    return render(
        request,
        "rooms/home.html",
        context={
            "rooms": all_rooms,
            "page": page,
            "page_count": page_count,
            "page_range": range(1, page_count),  # html에선 파이썬 코드가 안먹힘(range)
        },
    )
