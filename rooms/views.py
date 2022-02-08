from django.views.generic import ListView
from . import models


class HomeView(ListView):

    """ Homeview Definition """

    # ListView가 아래 model(Room 객체들)을 List 해줌
    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
