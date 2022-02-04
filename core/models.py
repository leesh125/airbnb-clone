from django.db import models

# 여러 app에서 쓰이는 공통 모델(데이터)을 담는 core
class TimeStampedModel(models.Model):

    """ Time Stamped Model """

    created = models.DateTimeField()
    update = models.DateTimeField()

    # 기타 사항 적는 클래스(추상 모델로써 db에는 core 공통 모델이 적용되지 않음)
    class Meta:
        # abstract model : model이긴 하나 DB에는 나타나지 않는 모델
        abstract = True