from django.db import models


class Interface(models.Model):
    name = models.CharField("名称", blank=False, max_length=200, default="")
    description = models.CharField("描述", blank=False, max_length=2000, default="")
    service_id = models.IntegerField("serviceId", default=0)
    context = models.TextField("内容", blank=False, max_length=4000, default="{}")  # json的转成字符串
