from django import forms
from . import models


class SearchForm(forms.Form):

    # form에 나타낼 model들 
    city = forms.CharField(initial="Anywhere")
    price = forms.IntegerField(required=False)
    room_type = forms.ModelChoiceField(queryset=models.RoomType.objects.all())