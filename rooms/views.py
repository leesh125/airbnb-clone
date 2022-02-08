from math import ceil
from django.shortcuts import render  # HttpResponse안에 html을 넣어서 보내줄 수 있다.
from django.core.paginator import Paginator
from . import models


# 장고는 Httprequest를 파이썬 객체로 변환해 준다.
def all_rooms(request):
    # request.Get : GET 메소드로 보내지는 요청 파라미터를 불러옴
    page = request.GET.get("page")
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10)  # room 객체들을 10개씩 끊음
    rooms = paginator.get_page(page)  # 해당 페이지 파라미터에 해당되는 room들을 가져옴
    return render(
        request,
        "rooms/home.html",
        context={"rooms": rooms},
    )
