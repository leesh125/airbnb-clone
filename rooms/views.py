from django.shortcuts import render  # HttpResponse안에 html을 넣어서 보내줄 수 있다.
from django.http import HttpResponse
from datetime import datetime


# 장고는 Httprequest를 파이썬 객체로 변환해 준다.
def all_rooms(request):
    now = datetime.now()
    hungry = True
    # all_rooms 이름의 템플릿을 반환해준다(ex.html)
    return render(
        request, "all_rooms.html", context={"now": now, "hungry": hungry}
    )  # 템플릿에 변수들을 같이 보냄
