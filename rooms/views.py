from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django_countries import countries
from . import models


class HomeView(ListView):

    """ Homeview Definition """

    # ListView가 아래 model(Room 객체들)을 List 해줌
    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"  # 불러오는 model object의 이름 설정


# Class Based View
class RoomDetail(DetailView):  # DetailView는 기본적으로 url argument로 pk를 찾음

    """ RoomDetail Definition """

    # view 한테 무슨 model을 원하는지 알려줘야함
    model = models.Room
    pk_url_kwargs = "potato"  # 지정한 이름으로 넘어올 매개변수 찾음


# Function Based View
# def room_detail(request, pk):  # 요청 파라미터로부터 온 pk도 같이 넘겨받음
#     try:
#         room = models.Room.objects.get(pk=pk)  # 매개변수로 넘어온 pk의 room 객체 가져오기
#         return render(request, "rooms/detail.html", {"room": room})
#     except models.Room.DoesNotExist:  # 매개변수로 넘어온 pk에 해당되는 room 객체가 없으면
#         raise Http404()  # 404 page 띄우기


def search(request):
    city = request.GET.get("city", "Anywhere")  # 요청 파라미터 city의 값을 읽어옴
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")  # 요청 파라미터 country의 값을 읽어옴
    room_type = int(request.GET.get("room_type", 0))  # 요청 파라미터 room_type의 값을 읽어옴
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    instant = request.GET.get("instant", False)
    super_host = request.GET.get("super_host", False)
    s_amenities = request.GET.getlist("amenities")  # getlist로 여러개 체크된 값의 id를 가져옴
    s_facilities = request.GET.getlist("facilities")  # getlist로 여러개 체크된 값의 id를 가져옴

    form = {  # 요청 파라미터로 넘어온 값
        "city": city,
        "s_room_type": room_type,
        "s_country": country,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "instant": instant,
        "super_host": super_host,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    return render(
        request,
        "rooms/search.html",
        {**form, **choices},
    )
