from django.shortcuts import render  # HttpResponse안에 html을 넣어서 보내줄 수 있다.
from django.http import HttpResponse
from . import models


# 장고는 Httprequest를 파이썬 객체로 변환해 준다.
def all_rooms(request):
    # request.Get : GET 메소드로 보내지는 요청 파라미터를 불러옴
    page = int(request.GET.get("page", 1))  # 파라미터 값을 가져옴(기본값 0)
    page_size = 10  # 보여질 room의 수
    limit = page_size * page  # 해당 페이지에서 보여질 room의 마지막 수
    offset = limit - page_size  # 해당 페이지에서 보여질 room의 첫번째 수
    all_rooms = models.Room.objects.all()[offset:limit]
    return render(request, "rooms/home.html", context={"rooms": all_rooms})
