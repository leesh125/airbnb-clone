from unicodedata import name
from django.urls import path
from . import views


app_name = "rooms"

# rooms/ 하위 url 경로에 int값이 오면(pk 변수에 대입) views.room_detail의 요청 파라미터로 pk를 넘겨줌
urlpatterns = [path("<int:pk>", views.RoomDetail.as_view(), name="detail")]
