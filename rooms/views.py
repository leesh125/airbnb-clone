from math import ceil
from django.shortcuts import render, redirect  # HttpResponse안에 html을 넣어서 보내줄 수 있다.
from django.core.paginator import Paginator, EmptyPage
from . import models


# 장고는 Httprequest를 파이썬 객체로 변환해 준다.
def all_rooms(request):
    # request.Get : GET 메소드로 보내지는 요청 파라미터를 불러옴
    page = request.GET.get("page", 1)
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5)
    try:
        rooms = paginator.page(int(page))
        return render(
            request,
            "rooms/home.html",
            context={"page": rooms},
        )
    except EmptyPage:
        return redirect("/")  # 빈 페이지가 요청되면 home으로 redirect
    # rooms = paginator.get_page(page)  # 현재 페이지에 대한 Paginator 객체 리턴
