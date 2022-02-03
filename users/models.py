from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models

# user 모델(테이블) 만들기(AbstractUser를 상속받아 기존 장고가 제공해주는 user의 필드 이용)
class User(AbstractUser):

    # 필드(컬럼) 생성 (생성 후 makemigrations -> migrate 해서 변경된 테이블을 적용해야함)
    bio = models.TextField(default="")
