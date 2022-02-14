from django.views.generic import ListView, DetailView, View
from django.shortcuts import render
from django.core.paginator import Paginator
from . import models, forms


class HomeView(ListView):

    """ Homeview Definition """

    # ListView가 아래 model(Room 객체들)을 List 해줌
    model = models.Room
    paginate_by = 12
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


class SearchView(View):

    """ SearchView Definition """

    def get(self, request):

        country = request.GET.get("country")  # country가 빈 값으로 올 경우

        if country:
            form = forms.SearchForm(request.GET)  # request 파라미터를 가져오고 기억할 수 있음

            if form.is_valid():  # form 이 에러가 없으면 True 리턴
                # cleaned_data: 선택한 값들을 가져옴(객체는 pk가 아닌 객체 그대로 가져옴)
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                rooms = models.Room.objects.filter(**filter_args)
                for amenity in amenities:
                    rooms = rooms.filter(amenities=amenity)

                for facility in facilities:
                    rooms = rooms.filter(facilities=facility)

                qs = rooms.order_by("created")

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)

                return render(
                    request, "rooms/search.html", {"form": form, "rooms": rooms}
                )
        else:  # country가 빈 값으로 올 경우
            form = forms.SearchForm()
            return render(request, "rooms/search.html", {"form": form})
