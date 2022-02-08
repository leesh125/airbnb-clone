from django.shortcuts import render  # HttpResponse안에 html을 넣어서 보내줄 수 있다.
from django.http import HttpResponse


# 장고는 Httprequest를 파이썬 객체로 변환해 준다.
def all_rooms(request):
    # all_rooms 이름의 템플릿을 반환해준다(ex.html)
    return render(request, "all_rooms")


"""
request의 전달과정은 다음과 같습니다.
user -----> web_server ----> WSGI-server -----> room_app

우선 user가 chrome이나 firefox와 같은 웹브라우저 를 이용하여 우리의 web_server에
request를 보내게 됩니다.

서버에서는 request를 받게되고, static 파일을 요구하는지? dynamic 파일을 요구하는지 확인 후
static이라면 웹 서버에서 바로 처리할 것 이고,
dynamic 이라면 WSGI-server에서 처리하게 될 것 입니다.

WSGI-서버 에서는 우리의 room app에 요청을 보내고, app에서 view를 통하여 처리 및 가공을 한후, 가공된 data를 template를 활용하여 rendering 하여 사용자의 화면으로 다시 response을 보내는 것 입니다.
"""