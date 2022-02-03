from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models

# user 모델(테이블) 만들기(AbstractUser를 상속받아 기존 장고가 제공해주는 user의 필드 이용)
class User(AbstractUser):

    """ Custom User Model"""

    # 필드(컬럼) 생성 (생성 후 makemigrations -> migrate 해서 변경된 테이블을 적용해야함)

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_ENGLISH = "english"
    LANGUAGE_KOREAN = "korean"

    LANGUAGE_CHOICES = (
        (LANGUAGE_ENGLISH, "English"),  # ("database에 넘어갈 값", "admin 패널 form에 보여질 값")
        (LANGUAGE_KOREAN, "Korean"),
    )

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = (
        (CURRENCY_USD, "USD"),
        (CURRENCY_KRW, "KRW"),
    )

    avatar = models.ImageField(null=True, blank=True)  # blank : 값을 입력 안해도됨
    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=10, null=True, blank=True
    )
    bio = models.TextField(
        default="", blank=True
    )  # default를 통해 기존에 있던 필드에 새로운 컬럼값을 설정 가능
    birthdate = models.DateField(null=True)
    language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=2, null=True, blank=True
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3, null=True, blank=True
    )
    superhost = models.BooleanField(default=False)