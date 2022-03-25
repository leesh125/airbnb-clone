from django.http import Http404
from django.views.generic import ListView, DetailView, View, UpdateView, FormView
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator, Page
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from users import mixins as user_mixins
from . import models, forms


class HomeView(ListView):

    """Homeview Definition"""

    # ListView가 아래 model(Room 객체들)을 List 해줌
    model = models.Room
    paginate_by = 12
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"  # 불러오는 model object의 이름 설정


# Class Based View
# class RoomDetail(DetailView):  # DetailView는 기본적으로 url argument로 pk를 찾음

#     """RoomDetail Definition"""

#     # view 한테 무슨 model을 원하는지 알려줘야함
#     model = models.Room


# Function Based View
@login_required
def room_detail(request, pk):  # 요청 파라미터로부터 온 pk도 같이 넘겨받음
    try:
        room = models.Room.objects.get(pk=pk)  # 매개변수로 넘어온 pk의 room 객체 가져오기
        return render(request, "rooms/room_detail.html", {"room": room})
    except models.Room.DoesNotExist:  # 매개변수로 넘어온 pk에 해당되는 room 객체가 없으면
        raise Http404()  # 404 page 띄우기


class SearchView(View):
    """Room search view"""

    def get(self, request):

        country = request.GET.get("country")

        if country:

            form = forms.SearchForm(request.GET)

            if form.is_valid():

                populated_data = form.cleaned_data

                city = populated_data.get("city")
                country = populated_data.get("country")
                room_type = populated_data.get("room_type")
                price = populated_data.get("price")
                guests = populated_data.get("guests")
                bedrooms = populated_data.get("bedrooms")
                beds = populated_data.get("beds")
                baths = populated_data.get("baths")
                instant_book = populated_data.get("instant_book")
                superhost = populated_data.get("superhost")
                amenities = populated_data.get("amenities")
                facilities = populated_data.get("facilities")

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

                qs = models.Room.objects.filter(**filter_args)

                for amenity in amenities:
                    qs = qs.filter(amenities=amenity)

                for facility in facilities:
                    qs = qs.filter(facilities=facility)

                qs = qs.order_by("-created")

                paginator = Paginator(qs, 10)

                page = int(request.GET.get("page", 1))

                rooms = paginator.get_page(page)

        else:

            form = forms.SearchForm()
            rooms = Page(
                [], number=0, paginator=Paginator([], 10)
            )  # just an empty Page for type match with if-case

        return render(request, "rooms/search.html", {"form": form, "rooms": rooms})


class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):

    model = models.Room
    template_name = "rooms/room_edit.html"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )

    # get_object() : room을 찾아서 보여줌
    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


# 로그인 한 사람만 접근 가능한 DetailView
class RoomPhotosView(user_mixins.LoggedInOnlyView, DetailView):

    model = models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


@login_required
def delete_photo(request, room_pk, photo_pk):
    user = request.user
    try:
        room = models.Room.objects.get(pk=room_pk)
        photo = models.Photo.objects.get(pk=photo_pk)
        if not (room.host.pk == user.pk and user.pk == photo.room.host.pk):
            messages.error(request, "Cant delete that photo")
        else:
            photo.delete()
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))


class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.Photo
    template_name = "rooms/photo_edit.html"
    pk_url_kwarg = "photo_pk"  # pk라는 이름이 아닌 다른 pk를 못찾기에 추가
    success_message = "Photo Updated"
    fields = ("caption",)

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:photos", kwargs={"pk": room_pk})

    def get_object(self, queryset=None):
        photo = super().get_object(queryset=queryset)
        if photo.room.host.pk != self.request.user.pk:
            raise Http404()
        return photo


class AddPhotoView(user_mixins.LoggedInOnlyView, FormView):

    template_name = "rooms/photo_create.html"
    form_class = forms.CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(self.request, "Photo Uploaded")
        return redirect(reverse("rooms:photos", kwargs={"pk": pk}))


class CreateRoomView(user_mixins.LoggedInOnlyView, FormView):

    form_class = forms.CreateRoomForm
    template_name = "rooms/room_create.html"

    def form_valid(self, form):
        room = form.save()
        room.host = self.request.user
        room.save()
        # many to many 필드 저장하기(db에 먼저 저장 후 호출해야한다)
        form.save_m2m()
        messages.success(self.request, "Room Uploaded")
        return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))
