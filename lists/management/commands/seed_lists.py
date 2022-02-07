import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists import models as list_models
from users import models as user_models
from rooms import models as room_models


NAME = "lists"

# 해당 py를 실행하고 BaseCommand를 상속받아 클래스를 작성하고 터미널에서 실행하면
# handle() 메소드를 실행한다.
class Command(BaseCommand):

    help = f"This command creates {NAME}"

    # 클래스를 실행할 때 사용할 수 있는 인자값 설정
    def add_arguments(self, parser):

        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help=f"how many {NAME} do you want to create",
        )

    # 클래스 실행시 인자값을 설정
    def handle(self, *args, **options):
        number = options.get("number")  # 인자로 준 number값 (50) 가져옴
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()
        # 50번동안 User 객체를 생성하는데 is_staff,is_superuser 를 false로 설정하고 생성
        seeder.add_entity(
            list_models.List,
            number,
            {
                "user": lambda x: random.choice(users),
            },
        )
        created = seeder.execute()
        cleaned = flatten(list(created.values()))
        for pk in cleaned:
            list_model = list_models.List.objects.get(pk=pk)
            # 0-5 ~ 6-30의 방 리스트 query set을 반환
            to_add = rooms[random.randint(0, 5) : random.randint(6, 30)]
            list_model.rooms.add(*to_add)  # *로 query set(array) 안에 있는 요소를 추가
        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))