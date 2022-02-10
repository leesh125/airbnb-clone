from django.views.generic import ListView
from django.http import Http404
from django.urls import reverse
from django.shortcuts import redirect, render
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
    try:
        room = models.Room.objects.get(pk=pk)  # 매개변수로 넘어온 pk의 room 객체 가져오기
        return render(request, "rooms/detail.html", {"room": room})
    except models.Room.DoesNotExist:  # 매개변수로 넘어온 pk에 해당되는 room 객체가 없으면
        raise Http404()  # 404 page 띄우기
