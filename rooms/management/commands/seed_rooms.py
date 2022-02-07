import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models

# 해당 py를 실행하고 BaseCommand를 상속받아 클래스를 작성하고 터미널에서 실행하면
# handle() 메소드를 실행한다.
class Command(BaseCommand):

    help = "This command creates rooms"

    # 클래스를 실행할 때 사용할 수 있는 인자값 설정
    def add_arguments(self, parser):

        parser.add_argument(
            "--number", default=2, type=int, help="how many rooms do you want to create"
        )

    # 클래스 실행시 인자값을 설정
    def handle(self, *args, **options):
        number = options.get("number")  # 인자로 준 number값 (50) 가져옴
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()  # db에 모든 User 가져오기
        room_types = room_models.RoomType.objects.all()
        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                # room의 host를 user에서 랜덤하게 배정
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "guests": lambda x: random.randint(1, 20),
                "price": lambda x: random.randint(1, 300),
                "beds": lambda x: random.randint(1, 5),
                "bedrooms": lambda x: random.randint(1, 5),
                "baths": lambda x: random.randint(1, 5),
            },
        )
        # room을 생성하면 db에 저장될때 pk값도 저장됨
        created_rooms = seeder.execute()
        # flatten을 사용하여 리스트안에 값을 가져옴(list 하나를 벗김)
        created_clean = flatten(list(created_rooms.values()))
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        rules = room_models.HouseRule.objects.all()
        for pk in created_clean:
            room = room_models.Room.objects.get(pk=pk)  # pk로 해당 pk의 room 찾기
            # 3 ~ 10 or 30개의 photo 적용
            for i in range(3, random.randint(10, 30)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"room_photos/{random.randint(1, 31)}.webp",
                )
            for a in amenities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.amenities.add(a)  # 다대다 필드에서 추가하는 방법(add)
            for f in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(f)
            for r in rules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.house_rules.add(r)
        self.stdout.write(self.style.SUCCESS(f"{number} Rooms created!"))