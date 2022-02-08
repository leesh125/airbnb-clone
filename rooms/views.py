from django.shortcuts import render  # HttpResponse안에 html을 넣어서 보내줄 수 있다.
from django.http import HttpResponse
from . import models


# 장고는 Httprequest를 파이썬 객체로 변환해 준다.
def all_rooms(request):
    all_rooms = models.Room.objects.all()
    return render(request, "rooms/home.html", context={"rooms": all_rooms})
