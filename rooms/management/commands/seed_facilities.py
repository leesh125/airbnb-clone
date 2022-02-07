from django.core.management.base import BaseCommand
from rooms import models as room_models

# 해당 py를 실행하고 BaseCommand를 상속받아 클래스를 작성하고 터미널에서 실행하면
# handle() 메소드를 실행한다.
class Command(BaseCommand):

    help = "This command creates facilities"

    """
    def add_arguments(self, parser):
        
        parser.add_argument("--times", help="how many times help you")
    """

    def handle(self, *args, **options):
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]
        for f in facilities:
            if not room_models.Facility.objects.filter(name=f):
                room_models.Facility.objects.create(name=f)
        self.stdout.write(self.style.SUCCESS(f'{len(facilities)} facilities created!'))