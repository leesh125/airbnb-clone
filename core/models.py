from django.db import models
from . import managers

# 여러 app에서 쓰이는 공통 모델(데이터)을 담는 core
class TimeStampedModel(models.Model):

    """ Time Stamped Model """

    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    objects = managers.CustomModelManager()  # 모든 app이 사용가능

    class Meta:
        abstract = True
