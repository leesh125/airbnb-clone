import uuid
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.shortcuts import reverse
from django.template.loader import render_to_string
from core import managers as core_managers


# user 모델(테이블) 만들기(AbstractUser를 상속받아 기존 장고가 제공해주는 user의 필드 이용)
class User(AbstractUser):

    """Custom User Model"""

    # 필드(컬럼) 생성 (생성 후 makemigrations -> migrate 해서 변경된 테이블을 적용해야함)

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
        (GENDER_OTHER, _("Other")),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "kr"

    LANGUAGE_CHOICES = (
        (LANGUAGE_ENGLISH, _("English")),
        (LANGUAGE_KOREAN, _("Korean")),
    )

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = (
        (CURRENCY_USD, _("USD")),
        (CURRENCY_KRW, _("KRW")),
    )

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_KAKAO = "kakao"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, _("Email")),
        (LOGIN_GITHUB, _("Github")),
        (LOGIN_KAKAO, _("Kakao")),
    )

    avatar = models.ImageField(upload_to="avatars", blank=True)  # blank : 값을 입력 안해도됨
    gender = models.CharField(
        _("gender"), choices=GENDER_CHOICES, max_length=10, blank=True
    )
    bio = models.TextField(
        _("bio"), blank=True
    )  # default를 통해 기존에 있던 필드에 새로운 컬럼값을 설정 가능
    birthdate = models.DateField(_("bithdate"), blank=True, null=True)
    language = models.CharField(
        _("language"),
        choices=LANGUAGE_CHOICES,
        max_length=2,
        blank=True,
        default=LANGUAGE_KOREAN,
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3, blank=True, default=CURRENCY_KRW
    )
    superhost = models.BooleanField(_("superhost"), default=False)
    email_verified = models.BooleanField(default=False)
    # 이메일 인증을 위해 랜덤 문자열 링크를 보내고 해당 유저가 그것을 클릭하면 이 문자열을 가진 user를 찾는다
    email_secret = models.CharField(max_length=120, default="", blank=True)
    login_method = models.CharField(
        max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )

    objects = core_managers.CustomUserManager()

    def get_absolute_url(self):

        return reverse("users:profile", kwargs={"pk": self.pk})

    # 이메일 인증을 view가 아닌 model에 둔 이유
    # : 이메일을 수정할 경우 다시 인증을 해야하기에
    def verify_email(self):
        # 이미 인증된 메일은 pass
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]  # 랜덤한 문자열
            self.email_secret = secret
            # render_to_string : template을 load해서 render함
            html_message = render_to_string(
                "emails/verify_email.html", {"secret": secret}
            )
            send_mail(
                _("Verify Airbnb Account"),
                strip_tags(html_message),  # html을 html 형태(태그)를 제외한 상태로 return
                settings.EMAIL_FROM,
                [self.email],
                fail_silently=False,
                html_message=html_message,  # message에 html을 적용
            )
            self.save()  # 해당 user의 email_secret 필드의 값을 저장
        return
