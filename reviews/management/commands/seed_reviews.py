import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews import models as review_models
from users import models as user_models
from rooms import models as room_models

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
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()
        # 50번동안 User 객체를 생성하는데 is_staff,is_superuser 를 false로 설정하고 생성
        seeder.add_entity(
            review_models.Review,
            number,
            {
                "accuracy": lambda x: random.randint(1, 5),
                "communication": lambda x: random.randint(1, 5),
                "cleanliness": lambda x: random.randint(1, 5),
                "location": lambda x: random.randint(1, 5),
                "check_in": lambda x: random.randint(1, 5),
                "value": lambda x: random.randint(1, 5),
                "room": lambda x: random.choice(rooms),
                "user": lambda x: random.choice(users),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} reviews created!"))