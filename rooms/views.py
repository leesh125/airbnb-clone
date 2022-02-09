from django.views.generic import ListView
from django.shortcuts import render
from . import models


class HomeView(ListView):

    """ Homeview Definition """

    # ListView가 아래 model(Room 객체들)을 List 해줌
    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"  # 불러오는 model object의 이름 설정


def room_detail(request, pk):  # 요청 파라미터로부터 온 pk도 같이 넘겨받음

    return render(request, "rooms/detail.html")