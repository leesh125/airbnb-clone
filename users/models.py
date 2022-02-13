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

    avatar = models.ImageField(upload_to="avatars", blank=True)  # blank : 값을 입력 안해도됨
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    bio = models.TextField(
        default="", blank=True
    )  # default를 통해 기존에 있던 필드에 새로운 컬럼값을 설정 가능
    birthdate = models.DateField(blank=True, null=True)
    language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=2, blank=True, default=LANGUAGE_KOREAN
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3, blank=True, default=CURRENCY_KRW
    )
    superhost = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)
    # 이메일 인증을 위해 랜덤 문자열 링크를 보내고 해당 유저가 그것을 클릭하면 이 문자열을 가진 user를 찾는다
    email_secret = models.CharField(max_length=120, default="", blank=True)

    # 이메일 인증을 view가 아닌 model에 둔 이유
    # : 이메일을 수정할 경우 다시 인증을 해야하기에
    def verify_email(self):
        pass