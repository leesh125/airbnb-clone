from django.core.management.base import BaseCommand
from rooms import models as room_models

# 해당 py를 실행하고 BaseCommand를 상속받아 클래스를 작성하고 터미널에서 실행하면
# handle() 메소드를 실행한다.
class Command(BaseCommand):

    help = "This command creates amenities"

    """
    def add_arguments(self, parser):
        
        parser.add_argument("--times", help="how many times help you")
    """

    def handle(self, *args, **options):
        amenities = [
            "Kitchen",
            "Heating",
            "Washer",
            "Wifi",
            "Indoor fireplace",
            "Iron",
            "Laptop friendly workspace",
            "Crib",
            "Self check-in",
            "Carbon monoxide detector",
            "Shampoo",
            "Air conditioning",
            "Dryer",
            "Breakfast",
            "Hangers",
            "Hair dryer",
            "TV",
            "High chair",
            "Smoke detector",
            "Private bathroom",
        ]
        for a in amenities:
            if not room_models.Amenity.objects.filter(name=a):
                room_models.Amenity.objects.create(name=a)
        self.stdout.write(self.style.SUCCESS("Amenities created!"))