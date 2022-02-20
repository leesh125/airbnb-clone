from django.db import models

# custom db 조작
class CustomModelManager(models.Manager):
    # 찾고자 하는 값이 없을때 error가 아닌 None
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None
