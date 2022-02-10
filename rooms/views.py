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
    instant = bool(request.GET.get("instant", False))
    superhost = bool(request.GET.get("superhost", False))
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
        "superhost": superhost,
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

    # 쿼리셋을 필터링
    filter_args = {}

    if city != "Anywhere":  # Anywhere가 아닌 어떤 도시가 입력되었다면
        filter_args[
            "city__startswith"
        ] = city  # filter 요소에 입력된 문자열로 시작되는 도시를 필터링할 수 있게끔

    filter_args["country"] = country  # 선택된 국가로 필터링

    if room_type != 0:  # room_type이 Any Kind(pk=0)이 아니라면
        # room_type의 pk가 요청 파라미터로 넘어온 pk와 같은지 필터
        filter_args["room_type__pk"] = room_type

    if price != 0:  # 가격이 입력되었다면
        filter_args["price_lte"] = price  # 파라미터로 넘어온 가격보다 작은 가격 필터링

    if guests != 0:  # 손님 수가 입력되었다면
        filter_args["guests_gte"] = guests  # 파라미터로 넘어온 손님 수보다 많은 손님을 수용하는 room 필터

    if bedrooms != 0:
        filter_args["bedrooms_gte"] = bedrooms

    if beds != 0:
        filter_args["beds_gte"] = beds

    if baths != 0:
        filter_args["baths_gte"] = baths

    if instant is True:
        filter_args["instant_book"] = True

    if superhost is True:
        filter_args["host__superhost"] = True

    # 선택된 amenity가 있으면
    if len(s_amenities) > 0:
        for s_amenity in s_amenities:
            filter_args["amenities__pk"] = int(s_amenity)  # 선택된 amenity의 pk를 filter

    if len(s_facilities) > 0:
        for s_facility in s_facilities:
            filter_args["facilities__pk"] = int(s_facility)

    rooms = models.Room.objects.filter(**filter_args)  # room 객체에 필터링

    return render(
        request,
        "rooms/search.html",
        {**form, **choices, "rooms": rooms},
    )
