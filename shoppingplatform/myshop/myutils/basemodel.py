from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:  # 模型是虚拟的
        abstract = True