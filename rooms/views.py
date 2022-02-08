from math import ceil
from django.shortcuts import render  # HttpResponse안에 html을 넣어서 보내줄 수 있다.
from django.core.paginator import Paginator
from . import models


# 장고는 Httprequest를 파이썬 객체로 변환해 준다.
def all_rooms(request):
    # request.Get : GET 메소드로 보내지는 요청 파라미터를 불러옴
    page = request.GET.get("page", 1)
    room_list = models.Room.objects.all()
    paginator = Paginator(
        room_list, 10, orphans=5
    )  # orphan(고아): 마지막 페이지에 5개이하 객체가 있으면 이전 페이지로 땡겨오기
    rooms = paginator.page(int(page))  # get_page가 아닌 page() 사용해보기
    # rooms = paginator.get_page(page)  # 현재 페이지에 대한 Paginator 객체 리턴

    return render(
        request,
        "rooms/home.html",
        context={"page": rooms},
    )
