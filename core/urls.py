from unicodedata import name
from django.urls import path
from rooms import views as room_views

app_name = "core"

urlpatterns = [
    # name: 나중에 해당 url을 처리할때 url전부를 하드코딩하는 것 이 아니라, 간편하게 해당 url을 지칭할 수 있다.
    path("", room_views.all_rooms, name="home")
]