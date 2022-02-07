import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models

# 해당 py를 실행하고 BaseCommand를 상속받아 클래스를 작성하고 터미널에서 실행하면
# handle() 메소드를 실행한다.
class Command(BaseCommand):

    help = "This command creates users"

    # 클래스를 실행할 때 사용할 수 있는 인자값 설정
    def add_arguments(self, parser):

        parser.add_argument(
            "--number", default=2, type=int, help="how many users do you want to create"
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
                "name": lambda x: seeder.faker.company(),
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
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} Rooms created!"))