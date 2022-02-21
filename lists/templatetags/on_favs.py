from django import template
from lists import models as list_models

register = template.Library()

# html에 쓰일 태그 등록
@register.simple_tag(takes_context=True)
def on_favs(context, room):
    user = context.request.user
    the_list = list_models.List.objects.get_or_none(
        user=user, name="My Favourite Houses"
    )  # "My Favourite Houses"의 리스트를 찾음
    if the_list is not None:
        return room in the_list.rooms.all()  # 방이 list에 있으면 True
    else:
        return False
